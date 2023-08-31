import datetime
from functools import wraps, reduce

from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.models.invoice import Invoice
from api.models.payment import Payment
from api.serializers.invoice import InvoiceSerializer


def admin_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        # For super-admins and admins
        if getattr(user, "role", None) in [
            "super-admin",
            "admin",
            "finance-admin",
        ]:
            return view_func(request, *args, **kwargs)

        return Response({"message": "Administrator is not authorized"}, status=403)

    return _wrapped_view


@api_view(["GET"])
def get_invoice(request, invoice_id):
    """
    Retrieve details of a specific invoice by its ID.

    Parameters:
    - request: The HTTP request object.
    - invoice_id: The ID of the invoice to retrieve.

    Returns:
    - If the invoice exists, returns the serialized invoice data.
    - If the invoice does not exist, returns an error response.

    HTTP Methods: GET
    """
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        invoice = payment_details(invoice)

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)
    except Invoice.DoesNotExist:
        return Response(
            {"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def create_invoice(request):
    """
    Create a new invoice.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the invoice is created successfully, returns the serialized invoice data.
    - If the invoice data is invalid, returns an error response.

    HTTP Methods: POST
    """
    invoice_number = generate_invoice_number()
    request.data["invoice_number"] = invoice_number
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@admin_access_required
def update_invoice(request, invoice_id):
    """
    Update an existing invoice by its ID.

    Parameters:
    - request: The HTTP request object.
    - invoice_id: The ID of the invoice to update.

    Returns:
    - If the invoice exists and the data is valid, returns the updated invoice data.
    - If the invoice does not exist or the data is invalid, returns an error response.

    HTTP Methods: POST
    """
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        return Response(
            {"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = InvoiceSerializer(invoice, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@admin_access_required
def delete_invoice(request, invoice_id):
    """
    Delete an existing invoice by its ID.

    Parameters:
    - request: The HTTP request object.
    - invoice_id: The ID of the invoice to delete.

    Returns:
    - If the invoice exists, deletes the invoice and returns a success response.
    - If the invoice does not exist, returns an error response.

    HTTP Methods: POST
    """
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        return Response(
            {"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND
        )

    invoice.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def generate_invoice_number():
    """
    Generate a unique invoice number with the prefix "INV-" followed by numbers based on the current date.

    Returns:
    - Unique invoice number string.

    Example:
    - INV-20230811-00001
    """
    today = datetime.date.today()
    invoice_count = Invoice.objects.filter(created_at__date=today).count()
    invoice_number = f"INV-{today.strftime('%Y%m%d')}-{invoice_count + 1:03d}"
    return invoice_number


def payment_details(invoice):
    """
    Calculate the payment details for an invoice.

    Args:
    - invoice (Invoice): The invoice object for which to calculate the payment details.

    Returns:
    - Invoice: The updated invoice object with total amount, paid amount, and balance calculated.
    """
    total_amount = 0
    paid_amount = 0
    status = "unpaid"

    for item in invoice.items:
        total_amount += int(item["quantity"]) * int(item["unit_price"])

    payments = Payment.objects.filter(invoice_number=invoice.invoice_number)

    for payment in payments:
        paid_amount += int(payment.amount)

    if paid_amount > total_amount or paid_amount == total_amount:
        status = "paid"

    invoice.total_amount = total_amount
    invoice.paid_amount = paid_amount
    invoice.balance = int(total_amount) - paid_amount
    invoice.status = status

    return invoice


@api_view(["POST"])
def search_invoices(request):
    """
    Search and retrieve a paginated list of invoices based on the provided search criteria.

    Args:
        request (Request): The HTTP POST request containing the search parameters.

    Returns:
        Response: A Response object containing the serialized data of the matching invoices.

    Raises:
        - KeyError: If the 'page' or 'limit' keys are not present in the request data.
        - Exception: If there is an error while processing the search or serialization.
    """
    user = request.user

    if getattr(user, "user_type", None) is None:
        return Response({"message": "User is not authorized"}, status=403)

    if getattr(user, "user_type", None) == "administrator" and getattr(
        user, "role", None
    ) not in [
        "super-admin",
        "admin",
        "finance-admin",
    ]:
        return Response({"message": "Administrator is not authorized"}, status=403)

    if getattr(user, "user_type", None) == "member" and (
        request.data.get("member_id") != user.id
    ):
        return Response(
            {"message": "Member is not authorized to view this invoice"}, status=403
        )

    query = get_invoices_query(request.data)

    offset = get_offset(request.data["page"], request.data["limit"])

    keyword = request.data.get("keyword")
    keyword_search = None

    if keyword:
        keywords = keyword.split()  # Split keyword into individual words
        keyword_queries = [
            Q(invoice_number__icontains=k) | Q(customer__icontains=k) for k in keywords
        ]

        keyword_search = reduce(lambda x, y: x | y, keyword_queries)

    if keyword_search:
        invoices = Invoice.objects.filter(keyword_search, **query).order_by(
            "-created_at"
        )[offset["start"] : offset["end"]]
    else:
        invoices = Invoice.objects.filter(**query).order_by("-created_at")[
            offset["start"] : offset["end"]
        ]

    for invoice in invoices:
        invoice = payment_details(invoice)

    serializer = InvoiceSerializer(invoices, many=True)

    return Response(serializer.data)


def get_invoices_query(data):
    query = {}

    if data["member_id"]:
        query["member_id"] = data["member_id"]

    if data["type"]:
        query["description__contains"] = data["type"]

    if data["status"]:
        query["status"] = data["status"]

    return query


def get_offset(page, limit):
    """
    Calculate the pagination range.

    Args:
        page (int): The current page number.
        limit (int): The maximum number of items per page.

    Returns:
        dict: A dictionary containing the start and end offsets for pagination.
    """
    end = limit * page
    start = end - limit
    start = start + 1 if start != 0 else start

    return {"start": start, "end": end}
