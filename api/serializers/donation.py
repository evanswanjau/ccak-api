from rest_framework import serializers
from api.models.donation import Donation


class DonationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Donation model.
    Provides validation and serialization/deserialization of Donation objects.
    """

    class Meta:
        model = Donation
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "company",
            "designation",
            "amount",
            "invoice_number",
            "status",
            "created_at",
            "last_updated",
        ]
