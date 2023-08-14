from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models.comment import Comment
from api.serializers.comment import CommentSerializer


@api_view(['POST'])
def create_comment(request):
    """
    Create a new comment.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the comment is created successfully, returns the generated token.
    - If the comment data is invalid, returns an error response.

    HTTP Methods: comment
    """
    if getattr(request.user, "subscription_status", None) != "inactive":
        return Response({"message": "Kindly renew you subscription"}, status=403)

    request.data["created_by"] = request.user.id
    # request.data["socialpost_id"] = request.data.get("socialpost")

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_comment(request, comment_id):
    """
    Update an existing comment by their comment ID.

    Parameters:
    - request: The HTTP request object.
    - comment_id: The ID of the comment to update.

    Returns:
    - If the comment exists and the data is valid, returns the updated comment data.
    - If the comment does not exist or the data is invalid, returns an error response.

    HTTP Methods: PATCH
    """
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({"error": "comment not found."}, status=status.HTTP_404_NOT_FOUND)

    request.data["created_by"] = request.user.id

    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_comment(request, comment_id):
    """
    Delete an existing comment by their comment ID.

    Parameters:
    - request: The HTTP request object.
    - comment_id: The ID of the comment to delete.

    Returns:
    - If the comment exists, deletes the comment and returns a success response.
    - If the comment does not exist, returns an error response.

    HTTP Methods: DELETE
    """
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)


    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def socialpost_comments(request, socialpost_id):
    """
    Retrieve all socialposts comments.

    Returns:
    - Serialized data for all comments for a single socialpost.
    """
    comments = Comment.objects.filter(socialpost=socialpost_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
