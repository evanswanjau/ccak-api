from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.models.invoice import Invoice
from api.models.payment import Payment
from api.serializers.invoice import InvoiceSerializer
import datetime


@api_view(['GET'])
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
        return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_invoices(request):
    """
    Retrieve all invoices.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Serialized data for all invoices.

    HTTP Methods: GET
    """
    invoices = Invoice.objects.all()
    for invoice in invoices:
        invoice = payment_details(invoice)
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)


@api_view(['POST'])
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
    request.data['invoice_number'] = invoice_number
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
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
    if getattr(request.user, "role", None) not in ["super-admin", "finance-admin", "admin"]:
        return Response({"message": "Administrator is not authorized"}, status=403)

    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = InvoiceSerializer(invoice, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
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
    if getattr(request.user, "role", None) not in ["super-admin", "finance-admin", "admin"]:
        return Response({"message": "Administrator is not authorized"}, status=403)

    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

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

    for item in invoice.items:
        total_amount += item['quantity'] * item['unit_price']

    invoice.total_amount = total_amount

    payments = Payment.objects.filter(invoice_number=invoice.invoice_number)
    for payment in payments:
        paid_amount += payment.amount

    invoice.paid_amount = paid_amount
    invoice.balance = total_amount - paid_amount

    return invoice


@api_view(['POST'])
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
    query = get_invoices_query(request.data)

    offset = get_offset(request.data['page'], request.data['limit'])
    data = Invoice.objects.filter(**query).order_by("-created_at")[offset["start"]:offset["end"]]

    for invoice in data:
        invoice = payment_details(invoice)

    serializer = InvoiceSerializer(data, many=True)

    return Response(serializer.data)


def get_invoices_query(data):
    query = {}

    if data['invoice_number']:
        query["invoice_number__contains"] = data['invoice_number']

    if data['type']:
        query["description__contains"] = data['type']

    if data['status']:
        query["status"] = data['status']

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
    start = (end - limit)
    start = start + 1 if start != 0 else start

    return {"start": start, "end": end}
