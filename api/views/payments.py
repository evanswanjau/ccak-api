import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models.payment import Payment
from api.serializers.payment import PaymentSerializer


class PaymentView(APIView):
    """
    API endpoint for managing payments.

    Methods:
    - GET: Retrieve all payments or a specific payment by its ID.
    - POST: Create a new payment.
    - PUT: Update an existing payment by its ID.
    - DELETE: Delete an existing payment by its ID.
    """

    def get(self, request, payment_id=None):
        """
        Retrieve all payments or a specific payment by its ID.

        Parameters:
        - request: The HTTP request object.
        - payment_id: The ID of the payment to retrieve (optional).

        Returns:
        - If payment_id is provided, returns the serialized payment data.
        - If payment_id is None, returns serialized data for all payments.

        HTTP Methods: GET
        """
        if payment_id is not None:
            return self.get_single_payment(payment_id)
        else:
            return self.get_all_payments()

    def get_single_payment(self, payment_id):
        """
        Retrieve details of an payment by its ID.

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

    def get_all_payments(self):
        """
        Retrieve all payments.

        Returns:
        - Serialized data for all payments.
        """
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new payment.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the payment is created successfully, returns the serialized payment data.
        - If the payment data is invalid, returns an error response.

        HTTP Methods: POST
        """
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, payment_id):
        """
        Update an existing payment by its ID.

        Parameters:
        - request: The HTTP request object.
        - payment_id: The ID of the payment to update.

        Returns:
        - If the payment exists and the data is valid, returns the updated payment data.
        - If the payment does not exist or the data is invalid, returns an error response.

        HTTP Methods: PATCH
        """
        try:
            payment = Payment.objects.get(pk=payment_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, payment_id):
        """
        Delete an existing payment by its ID.

        Parameters:
        - request: The HTTP request object.
        - payment_id: The ID of the payment to delete.

        Returns:
        - If the payment exists, deletes the payment and returns a success response.
        - If the payment does not exist, returns an error response.

        HTTP Methods: DELETE
        """
        try:
            payment = Payment.objects.get(pk=payment_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
