from rest_framework import serializers
from api.models.search import Search


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['id', 'keyword', 'table', 'category', 'technology', 'project_status', 'page', 'limit', 'ip_address',
                  'created_by', 'created_at']
