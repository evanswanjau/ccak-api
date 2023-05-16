from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'excerpt', 'content', 'published', 'category', 'image', 'project_status', 'event_date',
                  'venue', 'venue_link', 'attendees', 'gallery', 'documents', 'folder', 'access', 'views', 'status',
                  'step', 'created_by', 'created_by', 'last_updated']
