from rest_framework import serializers
from api.models.socialpost import SocialPost


class SocialPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPost
        fields = [
            "id",
            "post",
            "image",
            "likes",
            "status",
            "author",
            "company",
            "created_by",
            "created_at",
            "last_updated",
        ]
