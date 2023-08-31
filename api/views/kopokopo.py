import os
import k2connect

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models.kopokopo import Kopokopo
from api.serializers.kopokopo import KopokopoSerializer
from api.serializers.payment import PaymentSerializer
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("KOPOKOPO_CLIENT_ID")
CLIENT_SECRET = os.getenv("KOPOKOPO_CLIENT_SECRET")
BASE_URL = os.getenv("KOPOKOPO_BASE_URL")

# initialize the library
k2connect.initialize(CLIENT_ID, CLIENT_SECRET, BASE_URL)


def generate_token():
    """
    Generates an access token for the KopoKopo API.

    Returns:
    - The access token as a dictionary.

    Raises:
    - k2connect.TokenError: If there is an error generating the access token.
    """
    authenticator = k2connect.Tokens
    return authenticator.request_access_token()


@api_view(["POST"])
def receive_payments(request):
    """
    Process a payment request and initiate a payment using the KopoKopo API.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the payment request is successful, returns the payment request status.
    - If there is an error with the payment request, returns an error response.

    HTTP Methods: POST
    """
    token = generate_token()
    access_token = token.get("access_token")

    receive_payments_service = k2connect.ReceivePayments

    # initiate payment request
    mpesa_payment_location = receive_payments_service.create_payment_request(
        {
            "access_token": access_token,
            "callback_url": os.getenv("BACKEND_URL") + "/kopokopo/payment/process",
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "email": request.data.get("email"),
            "payment_channel": "MPESA",
            "phone_number": request.data.get("phone_number"),
            "till_number": os.getenv("KOPOKOPO_TILL"),
            "amount": request.data.get("amount"),
            "metadata": request.data.get("metadata"),
        }
    )

    payment_request_status = receive_payments_service.payment_request_status(
        access_token, mpesa_payment_location
    )
    return Response(payment_request_status)


@api_view(["POST"])
def process_payment(request):
    """
    Process the payment callback received from KopoKopo.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A JSON response with a message indicating successful payment processing.

    HTTP Methods: POST
    """
    return JsonResponse({"j-lo": "red"})


@api_view(["POST"])
def query_payment(request):
    """
    Query the status of a payment using the KopoKopo API.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the payment query is successful, returns the payment status.
    - If there is an error with the payment query, returns an error response.

    HTTP Methods: POST
    """
    token = generate_token()
    access_token = token.get("access_token")

    stk_service = k2connect.ReceivePayments

    url = (
        os.getenv("KOPOKOPO_BASE_URL")
        + "api/v1/incoming_payments/"
        + request.data.get("payment_id")
    )

    payment_request_status = stk_service.payment_request_status(access_token, url)
    return Response(payment_request_status)


@api_view(["GET"])
def buygoods_transaction_received_webhook(request):
    """
    Create a webhook subscription for the "buygoods_transaction_received" event.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the webhook subscription is successful, returns the created subscription.
    - If there is an error creating the webhook subscription, returns an error response.

    HTTP Methods: GET
    """
    token = generate_token()
    access_token = token.get("access_token")

    webhook_service = k2connect.Webhooks

    request_payload = {
        "access_token": access_token,
        "event_type": "buygoods_transaction_received",
        "webhook_endpoint": os.getenv("BACKEND_URL") + "/kopokopo/callback/buygoods",
        "scope": "till",
        "scope_reference": "112233",
    }

    customer_created_subscription = webhook_service.create_subscription(request_payload)

    return Response({"subscription": customer_created_subscription})


@api_view(["POST"])
def buygoods_transaction_received_callback(request):
    """
    Process the callback received from KopoKopo for the "buygoods_transaction_received" event.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the callback is processed successfully, returns a success response.
    - If there is an error processing the callback, returns an error response.

    HTTP Methods: POST
    """
    request.data["transaction_id"] = request.data["id"]
    request.data["timestamp"] = request.data["created_at"]

    print("we are here")

    serializer = KopokopoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        save_payment(request.data)
        return Response(
            {"message": "Payment received successfully"}, status=status.HTTP_201_CREATED
        )
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_kopokopo_payments(request):
    """
    Retrieve all kopokopo payments.

    Returns:
    - Serialized data for all kopokopo payments.
    """
    kopokopo_payments = Kopokopo.objects.all()
    serializer = KopokopoSerializer(kopokopo_payments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_single_kopokopo_payment(request, kopokopo_id):
    """
    Retrieve details of a kopokopo by its ID.

    Parameters:
    - kopokopo_id: The kopokopo_id of the invoice to retrieve.

    Returns:
    - If the kopokopo payment exists, returns the serialized kopokopo data.
    - If the kopokopo payment does not exist, returns an error response.
    """
    try:
        kopokopo = Kopokopo.objects.get(pk=kopokopo_id)
        serializer = KopokopoSerializer(kopokopo)
        return Response(serializer.data)
    except Kopokopo.DoesNotExist:
        return Response(
            {"error": "Kopokopo payment not found."}, status=status.HTTP_404_NOT_FOUND
        )


def save_payment(payment):
    payment_body = {
        "transaction_id": payment["event"]["resource"]["reference"],
        "method": "mpesa",
        "invoice_number": "",
        "timestamp": payment["event"]["resource"]["origination_time"],
        "amount": payment["event"]["resource"]["amount"],
        "name": payment["event"]["resource"]["sender_first_name"]
        + " "
        + payment["event"]["resource"]["sender_middle_name"]
        + " "
        + payment["event"]["resource"]["sender_last_name"],
        "phone_number": payment["event"]["resource"]["sender_phone_number"],
    }

    print(payment_body)
    serializer = PaymentSerializer(data=payment_body)
    if serializer.is_valid():
        print("we are ready to save")

        serializer.save()

        return Response(
            {"message": "Payment received successfully"}, status=status.HTTP_201_CREATED
        )

    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_invoice_status():
    # TODO 1. Get invoice amount
    # TODO 2. Calculate amounts
    # TODO 3. Update invoice status
    # TODO 4. Choose whether to activate user or not
    pass


def activate_member():
    # TODO 1. Get member details
    # TODO 2. Update details with the right amount
    pass
