from functools import wraps

from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models.member import Member
from api.models.subscriber import Subscriber
from api.models.post import Post
from api.models.administrator import Administrator
from api.models.invoice import Invoice
from api.models.donation import Donation


def admin_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if getattr(user, "role", None) in [
            "super-admin",
            "admin",
            "content-admin",
        ]:
            return view_func(request, *args, **kwargs)
        else:
            return Response({"message": "Administrator is not authorized"}, status=403)

    return _wrapped_view


@api_view(["GET"])
@admin_access_required
def general_stats(request):
    """
    Returns general statistics about the system's entities.

    Returns:
        Response: A dictionary containing counts of members, subscribers,
                  posts, and administrators.
    """
    response = {
        "members": Member.objects.all().count(),
        "subscribers": Subscriber.objects.all().count(),
        "posts": Post.objects.all().count(),
        "administrators": Administrator.objects.all().count(),
    }

    return Response(response)


@api_view(["GET"])
@admin_access_required
def money_stats(request):
    """
    Returns financial statistics about the system's transactions.

    Returns:
        Response: A dictionary containing completed and pending invoice payments,
                  donations, and total subscription payments.
    """
    response = {
        "completed": total_invoice_payments(Invoice.objects.filter(status="paid")),
        "pending": total_invoice_payments(Invoice.objects.filter(status="unpaid")),
        "donations": calculate_donations(Donation.objects.filter(status="paid")),
        "subscriptions": total_invoice_subscription_payments(),
    }

    return Response(response)


@api_view(["GET"])
@admin_access_required
def member_stats(request):
    """
    Returns statistics about the system's members based on their subscription status.

    Returns:
        Response: A dictionary containing counts of subscribed, unsubscribed,
                  registered, and unregistered members.
    """
    response = {
        "subscribed": Member.objects.filter(subscription_status="active").count(),
        "unsubscribed": Member.objects.filter(subscription_status="inactive").count(),
        "registered": Member.objects.filter(registration_status="registered").count(),
        "unregistered": Member.objects.filter(
            registration_status="unregistered"
        ).count(),
    }

    return Response(response)


def total_invoice_payments(invoices):
    total_amount = 0

    for invoice in invoices:
        for item in invoice.items:
            total_amount += int(item["quantity"]) * int(item["unit_price"])

    return total_amount


def calculate_donations(donations):
    total_amount = 0
    for donation in donations:
        total_amount += int(donation.amount)

    return total_amount


def total_invoice_subscription_payments():
    total_amount = 0
    invoices = Invoice.objects.filter(status="paid")

    for invoice in invoices:
        for item in invoice.items:
            if "subscription" in item["name"].lower():
                total_amount += int(item["quantity"]) * int(item["unit_price"])

    return total_amount
