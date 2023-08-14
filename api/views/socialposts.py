from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models.socialpost import SocialPost
from api.serializers.socialpost import SocialPostSerializer


@api_view(['GET'])
def get_socialpost(request, socialpost_id):
    """
    Retrieve details of a socialpost by their socialpost ID.

    Parameters:
    - socialpost_id: The ID of the socialpost to retrieve.

    Returns:
    - If the socialpost exists, returns the serialized socialpost data.
    - If the socialpost does not exist, returns an error response.
    """
    try:
        socialpost = SocialPost.objects.get(pk=socialpost_id)
        serializer = SocialPostSerializer(socialpost)
        return Response(serializer.data)
    except SocialPost.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_socialposts(request):
    """
    Retrieve all socialposts.

    Returns:
    - Serialized data for all socialposts.
    """
    socialposts = SocialPost.objects.all()
    serializer = SocialPostSerializer(socialposts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_socialpost(request):
    """
    Create a new socialpost.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the socialpost is created successfully, returns the generated token.
    - If the socialpost data is invalid, returns an error response.

    HTTP Methods: socialpost
    """
    if getattr(request.user, "subscription_status", None) != "active":
        return Response({"message": "Kindly renew you subscription"}, status=403)

    request.data["created_by"] = request.user.id

    serializer = SocialPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_socialpost(request, socialpost_id):
    """
    Update an existing socialpost by their socialpost ID.

    Parameters:
    - request: The HTTP request object.
    - socialpost_id: The ID of the socialpost to update.

    Returns:
    - If the socialpost exists and the data is valid, returns the updated socialpost data.
    - If the socialpost does not exist or the data is invalid, returns an error response.

    HTTP Methods: PATCH
    """
    try:
        socialpost = SocialPost.objects.get(pk=socialpost_id)
    except SocialPost.DoesNotExist:
        return Response({"error": "socialpost not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = SocialPostSerializer(socialpost, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_socialpost(request, socialpost_id):
    """
    Delete an existing socialpost by their socialpost ID.

    Parameters:
    - request: The HTTP request object.
    - socialpost_id: The ID of the socialpost to delete.

    Returns:
    - If the socialpost exists, deletes the socialpost and returns a success response.
    - If the socialpost does not exist, returns an error response.

    HTTP Methods: DELETE
    """
    try:
        socialpost = SocialPost.objects.get(pk=socialpost_id)
    except SocialPost.DoesNotExist:
        return Response({"error": "socialpost not found."}, status=status.HTTP_404_NOT_FOUND)

    socialpost.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def member_socialposts(request, member_id):
    """
    Retrieve all member socialposts.

    Returns:
    - Serialized data for all socialposts for a single member.
    """
    socialposts = SocialPost.objects.filter(created_by=member_id)
    serializer = SocialPostSerializer(socialposts, many=True)
    return Response(serializer.data)
