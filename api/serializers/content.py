from rest_framework import serializers
from api.models.content import Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            "id",
            "page",
            "section",
            "content",
            "created_at",
            "last_updated",
        ]
