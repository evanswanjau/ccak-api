import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models.invoice import Invoice
from api.serializers.invoice import InvoiceSerializer


class InvoiceView(APIView):
    """
    API endpoint for managing invoices.

    Methods:
    - GET: Retrieve all invoices or a specific invoice by its ID.
    - POST: Create a new invoice.
    - PUT: Update an existing invoice by its ID.
    - DELETE: Delete an existing invoice by its ID.
    """

    def get(self, request, invoice_id=None):
        """
        Retrieve all invoices or a specific invoice by its ID.

        Parameters:
        - request: The HTTP request object.
        - invoice_id: The ID of the invoice to retrieve (optional).

        Returns:
        - If invoice_id is provided, returns the serialized invoice data.
        - If invoice_id is None, returns serialized data for all invoices.

        HTTP Methods: GET
        """
        if invoice_id is not None:
            return self.get_single_invoice(invoice_id)
        else:
            return self.get_all_invoices()

    def get_single_invoice(self, invoice_id):
        """
        Retrieve details of an invoice by its ID.

        Parameters:
        - invoice_id: The ID of the invoice to retrieve.

        Returns:
        - If the invoice exists, returns the serialized invoice data.
        - If the invoice does not exist, returns an error response.
        """
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_all_invoices(self):
        """
        Retrieve all invoices.

        Returns:
        - Serialized data for all invoices.
        """
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new invoice.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the invoice is created successfully, returns the serialized invoice data.
        - If the invoice data is invalid, returns an error response.

        HTTP Methods: POST
        """
        invoice_number = self.generate_invoice_number(self)
        request.data['invoice_number'] = invoice_number

        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, invoice_id):
        """
        Update an existing invoice by its ID.

        Parameters:
        - request: The HTTP request object.
        - invoice_id: The ID of the invoice to update.

        Returns:
        - If the invoice exists and the data is valid, returns the updated invoice data.
        - If the invoice does not exist or the data is invalid, returns an error response.

        HTTP Methods: PATCH
        """
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, invoice_id):
        """
        Delete an existing invoice by its ID.

        Parameters:
        - request: The HTTP request object.
        - invoice_id: The ID of the invoice to delete.

        Returns:
        - If the invoice exists, deletes the invoice and returns a success response.
        - If the invoice does not exist, returns an error response.

        HTTP Methods: DELETE
        """
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def generate_invoice_number(self):
        """
        Generate a unique invoice number with the prefix "INV-" followed by numbers based on the current date.

        Returns:
        - Unique invoice number string.

        Example:
        - INV-20230615-00001
        """
        today = datetime.date.today()
        invoice_count = Invoice.objects.filter(created_at__date=today).count()
        invoice_number = f"INV-{today.strftime('%Y%m%d')}-{invoice_count + 1:03d}"
        return invoice_number
