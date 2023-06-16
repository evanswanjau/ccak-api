from rest_framework import serializers
from api.models.kopokopo import Kopokopo


class KopokopoSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Post model.
    Provides serialization/deserialization of Post objects.
    """

    class Meta:
        model = Kopokopo
        fields = ['id', 'topic', 'transaction_id', 'timestamp', 'event', 'links', 'created_at', 'last_updated']
