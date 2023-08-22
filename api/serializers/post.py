from rest_framework import serializers
from api.models.post import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Post model.
    Provides serialization/deserialization of Post objects.
    """

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "excerpt",
            "tags",
            "content",
            "published",
            "category",
            "image",
            "project_status",
            "event_date",
            "venue",
            "venue_link",
            "attendees",
            "files",
            "folder",
            "access",
            "views",
            "status",
            "step",
            "author",
            "created_by",
            "created_at",
            "last_updated",
        ]
