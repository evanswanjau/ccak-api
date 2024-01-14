from functools import wraps

from django.db.models import Q
from functools import reduce
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from api.models.socialpost import SocialPost
from api.models.member import Member
from api.serializers.socialpost import SocialPostSerializer


def admin_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        socialpost_id = kwargs.get("socialpost_id")

        if getattr(user, "role", None) in [
            "super-admin",
            "admin",
            "content-admin",
        ]:
            return view_func(request, *args, **kwargs)

        socialpost = SocialPost.objects.get(pk=socialpost_id)
        # Allow member to edit or delete their own socialpost
        if (
            getattr(user, "user_type", None) == "member"
            and socialpost.created_by_id == user.id
        ):
            return view_func(request, *args, **kwargs)

        return Response({"message": "User is not authorized"}, status=403)

    return _wrapped_view


@api_view(["GET"])
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

        member = Member.objects.get(pk=socialpost.created_by_id)
        socialpost.author = f"{member.first_name} {member.last_name}"
        socialpost.company = member.company
        socialpost.logo = member.logo

        serializer = SocialPostSerializer(socialpost)
        return Response(serializer.data)
    except SocialPost.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
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
    if getattr(request.user, "user_type", None) != "member":
        return Response({"message": "User is not authorized"}, status=403)

    if getattr(request.user, "subscription_status", None) != "active":
        return Response({"message": "Kindly renew your subscription"}, status=403)

    request.data["created_by"] = request.user.id

    serializer = SocialPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
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
        if getattr(request.user, "user_type", None) is None:
            return Response({"message": "User is not authorized"}, status=403)

        if getattr(request.user, "user_type", None) == "administrator" and getattr(
            request.user, "role", None
        ) not in [
            "super-admin",
            "admin",
            "content-admin",
        ]:
            return Response({"message": "Administrator is not authorized"}, status=403)

        socialpost = SocialPost.objects.get(pk=socialpost_id)

        # Allow member to edit or delete their own socialpost
        if (
            getattr(request.user, "user_type", None) == "member"
            and socialpost.created_by_id != request.user.id
        ):
            return Response({"message": "Member is not authorized"}, status=403)

    except SocialPost.DoesNotExist:
        return Response(
            {"error": "socialpost not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = SocialPostSerializer(socialpost, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
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
        if getattr(request.user, "user_type", None) is None:
            return Response({"message": "User is not authorized"}, status=403)

        if getattr(request.user, "user_type", None) == "administrator" and getattr(
            request.user, "role", None
        ) not in [
            "super-admin",
            "admin",
            "content-admin",
        ]:
            return Response({"message": "Administrator is not authorized"}, status=403)

        socialpost = SocialPost.objects.get(pk=socialpost_id)

        # Allow member to edit or delete their own socialpost
        if (
            getattr(request.user, "user_type", None) == "member"
            and socialpost.created_by_id != request.user.id
        ):
            return Response({"message": "Member is not authorized"}, status=403)

    except SocialPost.DoesNotExist:
        return Response(
            {"error": "socialpost not found."}, status=status.HTTP_404_NOT_FOUND
        )

    socialpost.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def member_socialposts(request, member_id):
    """
    Retrieve all member socialposts.

    Returns:
    - Serialized data for all socialposts for a single member.
    """
    socialposts = SocialPost.objects.filter(created_by=member_id).order_by(
        "-created_at"
    )

    for socialpost in socialposts:
        member = Member.objects.get(pk=socialpost.created_by_id)
        socialpost.author = f"{member.first_name} {member.last_name}"
        socialpost.company = member.company
        socialpost.logo = member.logo

    serializer = SocialPostSerializer(socialposts, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def search_posts(request):
    """
    Search posts based on specified criteria.
    """
    query = get_socialposts_query(request.data)

    keyword = request.data.get("keyword")
    keyword_search = None

    if keyword:
        keywords = keyword.split()
        keyword_queries = [
            Q(post__icontains=k)
            for k in keywords
        ]

        keyword_search = reduce(lambda x, y: x | y, keyword_queries)

    if keyword_search:
        data = SocialPost.objects.filter(keyword_search, **query).order_by("-created_at")
    else:
        data = SocialPost.objects.filter(**query).order_by("-created_at")

    paginator = PageNumberPagination()
    paginator.page_size = request.data["limit"]
    paginated_posts = paginator.paginate_queryset(data, request)
    post_serializer = SocialPostSerializer(paginated_posts, many=True)

    return paginator.get_paginated_response(post_serializer.data)


def get_socialposts_query(data):
    query = {}

    if data["keyword"]:
        query["post__contains"] = data["keyword"]

    if data["status"]:
        query["status"] = data["status"]

    return query
