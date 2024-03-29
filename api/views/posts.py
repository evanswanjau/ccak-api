from datetime import datetime
from functools import wraps

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from api.models.post import Post
from api.models.administrator import Administrator
from api.serializers.post import PostSerializer
from api.serializers.post import AllPostsSerializer
from django.db.models import Case, When, Value
from django.db.models import IntegerField
from django.utils import timezone


def admin_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if getattr(user, "role", None) in [
            "super-admin",
            "admin",
            "content-admin",
        ]:
            return view_func(request, *args, **kwargs)
        else:
            return Response({"message": "Administrator is not authorized"}, status=403)

    return _wrapped_view


@api_view(["GET"])
def get_post(request, post_id):
    """
    Retrieve details of a post by their post ID.

    Parameters:
    - post_id: The ID of the post to retrieve.

    Returns:
    - If the post exists, returns the serialized post data.
    - If the post does not exist, returns an error response.
    """
    try:
        post = Post.objects.get(pk=post_id)

        if getattr(request.user, "user_type", None) != "administrator":
            # Update view count
            post.views += 1
            post.save()  # Save the updated view count

        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@admin_access_required
def create_post(request):
    """
    Create a new post.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the post is created successfully, returns the generated token.
    - If the post data is invalid, returns an error response.

    HTTP Methods: POST
    """
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data["created_by"] = request.user

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@admin_access_required
def update_post(request, post_id):
    """
    Update an existing post by their post ID.

    Parameters:
    - request: The HTTP request object.
    - post_id: The ID of the post to update.

    Returns:
    - If the post exists and the data is valid, returns the updated post data.
    - If the post does not exist or the data is invalid, returns an error response.

    HTTP Methods: PATCH
    """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@admin_access_required
def delete_post(request, post_id):
    """
    Delete an existing post by their post ID.

    Parameters:
    - request: The HTTP request object.
    - post_id: The ID of the post to delete.

    Returns:
    - If the post exists, deletes the post and returns a success response.
    - If the post does not exist, returns an error response.

    HTTP Methods: DELETE
    """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def search_posts(request):
    """
    Search view that searches for posts based on specified criteria.

    Request Method: POST

    Request Body Parameters:
        - keyword (string): The keyword to search for in post titles.
        - category (string): The category of posts to search in.
        - project_status (string): (Optional) The status of project posts to filter by.
        - technology (string): (Optional) The member technology to filter by.
        - page (integer): The page number for pagination.
        - limit (integer): The maximum number of results per page.

    Returns:
        - Response with paginated list of matching post objects.

    Algorithm:
        1. Extract the keyword, category, project_status, page, and limit from the request data.
        2. Create a search query based on the provided criteria.
        3. Perform a database query to retrieve posts matching the query.
        4. Apply pagination to the query results based on the page and limit.
        5. Serialize the paginated posts data.
        6. Return the paginated posts as a JSON response.

    Note:
        - The search query filters posts based on the keyword, category, and project status (if provided).
        - Posts are ordered by 'published' if the category is 'events', otherwise by 'event_date'.
        - The pagination is implemented using the 'page' and 'limit' parameters.
        - The response includes the paginated list of post objects.
    """
    query = get_posts_query(request.data)

    category = request.data.get("category")
    if category in ["events"]:
         data = Post.objects.filter(**query).annotate(
             past_due=Case(
                 When(event_date__lt=timezone.now(), then=Value(1)),
                 default=Value(0),
                 output_field=IntegerField(),
                 )).order_by('past_due', '-event_date')
    else:
        data = Post.objects.filter(**query).order_by("-published")

    for item in data:
        author = Administrator.objects.get(pk=item.created_by_id)
        item.author = f"{author.first_name} {author.last_name}"

    paginator = PageNumberPagination()
    paginator.page_size = request.data["limit"]
    paginated_posts = paginator.paginate_queryset(data, request)
    post_serializer = AllPostsSerializer(paginated_posts, many=True)

    return paginator.get_paginated_response(post_serializer.data)


def get_posts_query(data):
    query = {}

    if data["keyword"]:
        query["title__contains"] = data["keyword"]

    if data["category"]:
        query["category"] = data["category"]

    if data["category"] == "projects" and data["project_status"]:
        query["project_status"] = data["project_status"]

    if data["access"]:
        query["access"] = data["access"]
        if data["access"] == "public":
            query["published__lt"] = datetime.today()

    if data["status"]:
        query["status"] = data["status"]

    return query
