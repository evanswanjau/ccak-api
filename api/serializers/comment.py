from rest_framework import serializers
from api.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'socialpost', 'status', 'created_by', 'created_at', 'last_updated']
