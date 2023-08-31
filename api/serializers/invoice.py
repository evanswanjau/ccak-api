from rest_framework import serializers
from api.models.invoice import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invoice model.
    Serializes the Invoice model fields for API interactions.
    """

    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, read_only=True
    )
    paid_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, read_only=True
    )
    balance = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, read_only=True
    )

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "description",
            "items",
            "status",
            "member_id",
            "donation_id",
            "customer",
            "total_amount",
            "paid_amount",
            "balance",
            "created_by",
            "created_at",
            "last_updated",
        ]
