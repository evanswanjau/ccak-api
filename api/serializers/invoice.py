from rest_framework import serializers
from api.models.invoice import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invoice model.
    Serializes the Invoice model fields for API interactions.
    """

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'description', 'items', 'status', 'member_id', 'customer', 'created_by',
                  'created_at', 'last_updated']
