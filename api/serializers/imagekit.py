from rest_framework import serializers


class ImagekitSerializer(serializers.Serializer):
    file_id = serializers.CharField()
    name = serializers.CharField()
    url = serializers.URLField()
    thumbnail_url = serializers.URLField()
    height = serializers.IntegerField()
    width = serializers.IntegerField()
    size = serializers.IntegerField()
    file_path = serializers.CharField()
    tags = serializers.ListField(allow_null=True)
    is_private_file = serializers.BooleanField()
    custom_coordinates = serializers.CharField(allow_null=True)
    custom_metadata = serializers.CharField(allow_null=True)
    extension_status = serializers.CharField(allow_null=True)
    file_type = serializers.CharField()
    orientation = serializers.CharField(allow_null=True)
