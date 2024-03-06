from functools import wraps, reduce
from dotenv import load_dotenv
import os

from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from api.models.payment import Payment
from api.models.invoice import Invoice
from api.models.member import Member
from api.models.donation import Donation
from api.serializers.payment import PaymentSerializer
from api.serializers.invoice import InvoiceSerializer
from api.utils.email import send_email

load_dotenv()

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
@admin_access_required
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
        return Response(
            {"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
@admin_access_required
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


@api_view(["POST"])
@admin_access_required
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
    try:
        payment = Payment.objects.get(pk=payment_id)
    except Payment.DoesNotExist:
        return Response(
            {"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = PaymentSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        if payment.invoice_number:
            update_invoice_status(payment.invoice_number)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@admin_access_required
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
    try:
        payment = Payment.objects.get(pk=payment_id)
        if payment.invoice_number:
            update_invoice_status(payment.invoice_number)
    except Payment.DoesNotExist:
        return Response(
            {"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND
        )

    payment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def activate_mpesa_payment(request):
    payments = Payment.objects.filter(transaction_id=request.data.get("transaction_id"))

    for payment in payments:
        payment.invoice_number = request.data.get("invoice_number")
        payment.email = request.data.get("email")
        payment.save()

    update_invoice_status(request.data.get("invoice_number"))

    serializer = PaymentSerializer(payments, many=True)

    return Response(serializer.data)


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

    invoice = Invoice.objects.get(invoice_number=invoice_number)

    for item in invoice.items:
        total_amount += int(item["quantity"]) * int(item["unit_price"])

    payments = Payment.objects.filter(invoice_number=invoice.invoice_number)

    for payment in payments:
        paid_amount += int(payment.amount)

    invoice.total_amount = total_amount
    invoice.paid_amount = paid_amount
    invoice.balance = total_amount - paid_amount
    invoice.status = "unpaid"

    if paid_amount > total_amount or paid_amount == total_amount:
        invoice.status = "paid"

        if invoice.description == "Donation":
            donation_status_update(invoice.donation_id)
        if invoice.description == "Annual Subscription":
            subscribe_member(invoice.member_id)
        if invoice.description == "Member Registration and Annual Subscription":
            subscribe_activate_member(invoice.member_id)

        invoice_completion_successful(invoice)

    invoice.save()

    serializer = InvoiceSerializer(invoice)
    return serializer.data


@api_view(["POST"])
def search_payments(request):
    query = get_payments_query(request.data)

    keyword = request.data.get("keyword")
    keyword_search = None

    if keyword:
        keywords = keyword.split()  # Split keyword into individual words
        keyword_queries = [
            Q(invoice_number__icontains=k)
            | Q(transaction_id__icontains=k)
            | Q(name__icontains=k)
            | Q(phone_number__icontains=k)
            for k in keywords
        ]

        keyword_search = reduce(lambda x, y: x | y, keyword_queries)

    if keyword_search:
        data = Payment.objects.filter(keyword_search, **query).order_by("-created_at")
    else:
        data = Payment.objects.filter(**query).order_by("-created_at")

    paginator = PageNumberPagination()
    paginator.page_size = request.data["limit"]
    paginated_posts = paginator.paginate_queryset(data, request)
    post_serializer = PaymentSerializer(paginated_posts, many=True)

    return paginator.get_paginated_response(post_serializer.data)


def get_payments_query(data):
    query = {}

    if data["method"]:
        query["method"] = data["method"]

    return query


def subscribe_member(member_id):
    member = Member.objects.get(pk=member_id)

    if member.subscription_status == "inactive":
        member.subscription_status = "active"
        member.save()

        subject = "Your Annual Subscription to CCAK: Successfully Renewed!"
        context = {
            "recipient_name": member.first_name,
        }
        send_email(member.email, subject, context, "member_annual_subscription.html")


def subscribe_activate_member(member_id):
    member = Member.objects.get(pk=member_id)

    if (
        member.subscription_status == "inactive"
        and member.registration_status == "unregistered"
    ):
        member.registration_status = "registered"
        member.subscription_status = "active"
        member.save()

        subject = "Your CCAK Member Registration and Annual Subscription"
        context = {
            "recipient_name": member.first_name,
        }

        send_email(
            member.email,
            subject,
            context,
            "member_registration_annual_subscription.html",
        )


def donation_status_update(donation_id):
    donation = Donation.objects.get(pk=donation_id)

    if donation.status == "unpaid":
        donation.status = "paid"
        donation.save()

        subject = "Your CCAK Donation has been received"
        context = {
            "recipient_name": donation.first_name,
        }

        send_email(
            donation.email,
            subject,
            context,
            "donation_received.html",
        )


def invoice_completion_successful(invoice):
    subject = f"Payment Completed for #{invoice.invoice_number}"
    context = {
        "invoice": invoice,
    }
    return send_email(
        os.getenv("EMAIL_RECIPIENT"),
        subject,
        context,
        "paid_invoice.html",
    )
