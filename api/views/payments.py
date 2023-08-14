from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.models.payment import Payment
from api.models.invoice import Invoice
from api.serializers.payment import PaymentSerializer
from api.serializers.invoice import InvoiceSerializer


@api_view(['GET'])
def get_payment(request, payment_id):
    """
    Retrieve details of a specific payment by its ID.

    Parameters:
    - payment_id: The ID of the payment to retrieve.

    Returns:
    - If the payment exists, returns the serialized payment data.
    - If the payment does not exist, returns an error response.
    """
    try:
        payment = Payment.objects.get(pk=payment_id)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_payments(request):
    """
    Retrieve all payments.

    Returns:
    - Serialized data for all payments.
    """
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_payment(request):
    """
    Create a new payment.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the payment is created successfully, returns the serialized payment data.
    - If the payment data is invalid, returns an error response.
    """
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        if request.data.get("invoice_number"):
            update_invoice_status(request.data.get("invoice_number"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_payment(request, payment_id):
    """
    Update an existing payment by its ID.

    Parameters:
    - request: The HTTP request object.
    - payment_id: The ID of the payment to update.

    Returns:
    - If the payment exists and the data is valid, returns the updated payment data.
    - If the payment does not exist or the data is invalid, returns an error response.
    """
    if getattr(request.user, "role", None) not in ["super-admin", "finance-admin", "admin"]:
        return Response({"message": "Administrator is not authorized"}, status=403)

    try:
        payment = Payment.objects.get(pk=payment_id)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PaymentSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        if payment.invoice_number:
            update_invoice_status(payment.invoice_number)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_payment(request, payment_id):
    """
    Delete an existing payment by its ID.

    Parameters:
    - request: The HTTP request object.
    - payment_id: The ID of the payment to delete.

    Returns:
    - If the payment exists, deletes the payment and returns a success response.
    - If the payment does not exist, returns an error response.
    """
    if getattr(request.user, "role", None) not in ["super-admin", "finance-admin", "admin"]:
        return Response({"message": "Administrator is not authorized"}, status=403)

    try:
        payment = Payment.objects.get(pk=payment_id)
        if payment.invoice_number:
            update_invoice_status(payment.invoice_number)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

    payment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def update_invoice_status(invoice_number):
    """
    Update the status of an invoice based on the payment details.

    Parameters:
    - invoice_number: The invoice number for which to update the status.

    Returns:
    - Serialized data of the updated invoice.
    """
    total_amount = 0
    paid_amount = 0
    status = "unpaid"

    invoice = Invoice.objects.get(invoice_number=invoice_number)
    for item in invoice.items:
        total_amount += item["quantity"] * item["unit_price"]

    payments = Payment.objects.filter(invoice_number=invoice.invoice_number)
    for payment in payments:
        paid_amount += int(payment.amount)

    if total_amount == paid_amount or total_amount < paid_amount:
        status = "paid"

    invoice.status = status
    invoice.save()
    serializer = InvoiceSerializer(invoice)
    return serializer.data


@api_view(['POST'])
def search_payments(request):
    query = get_payments_query(request.data)

    offset = get_offset(request.data['page'], request.data['limit'])
    data = Payment.objects.filter(**query).order_by("-created_at")[offset["start"]:offset["end"]]

    serializer = PaymentSerializer(data, many=True)

    return Response(serializer.data)


def get_payments_query(data):
    query = {}

    if data['transaction_id']:
        query["transaction_id__contains"] = data['transaction_id']

    if data['method']:
        query["method"] = data['method']

    if data['invoice_number']:
        query["invoice_number__contains"] = data['invoice_number']

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
