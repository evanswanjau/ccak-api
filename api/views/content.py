from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models.content import Content
from api.serializers.content import ContentSerializer


@api_view(["POST"])
def create_content(request):
    """
    Create new content.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the content is created successfully, returns a response.
    - If the content data is invalid, returns an error response.

    HTTP Methods: content
    """
    serializer = ContentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def update_content(request, content_id):
    """
    Update existing content by their content ID.

    Parameters:
    - request: The HTTP request object.
    - content_id: The ID of the content to update.

    Returns:
    - If the content exists and the data is valid, returns the updated content data.
    - If the content does not exist or the data is invalid, returns an error response.

    HTTP Methods: PATCH
    """
    try:
        content = Content.objects.get(pk=content_id)
    except content.DoesNotExist:
        return Response(
            {"error": "content not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ContentSerializer(content, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_content(request, content_id):
    """
    Delete existing content by their content ID.

    Parameters:
    - request: The HTTP request object.
    - content_id: The ID of the content to delete.

    Returns:
    - If the content exists, deletes the content and returns a success response.
    - If the content does not exist, returns an error response.

    HTTP Methods: DELETE
    """
    try:
        content = Content.objects.get(pk=content_id)
    except content.DoesNotExist:
        return Response(
            {"error": "content not found."}, status=status.HTTP_404_NOT_FOUND
        )

    content.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def search_content(request):
    """
    Search contents.

    Returns:
    - Serialized data for contents.
    """
    query = {
        'page': request.data.get('page')
    }

    if request.data.get('section'):
        query["section"] = request.data.get('section')

    contents = Content.objects.filter(**query).order_by("section")

    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)
