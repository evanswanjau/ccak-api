from rest_framework import serializers
from api.models.payment import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

    class Meta:
        model = Payment
        fields = ['id', 'transaction_id', 'method', 'invoice_number', 'timestamp', 'amount', 'paid_by', 'created_by',
                  'created_at', 'last_updated']
