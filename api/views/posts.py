from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models.post import Post
from api.serializers.post import PostSerializer


class PostView(APIView):
    """
    API endpoint for managing posts.

    Methods:
    - GET: Retrieve all posts or a specific post by their post ID.
    - POST: Create a new post.
    - PUT: Update an existing post by their post ID.
    - DELETE: Delete an existing post by their post ID.
    """

    def get(self, request, post_id=None):
        """
        Retrieve all posts or a specific post by their post ID.

        Parameters:
        - request: The HTTP request object.
        - post_id: The ID of the post to retrieve (optional).

        Returns:
        - If post_id is provided, returns the serialized post data.
        - If post_id is None, returns serialized data for all posts.

        HTTP Methods: GET
        """
        if post_id is not None:
            return self.get_single_post(post_id)
        else:
            return self.get_all_posts()

    def get_single_post(self, post_id):
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
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_all_posts(self):
        """
        Retrieve all posts.

        Returns:
        - Serialized data for all posts.
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, post_id):
        """
        Update an existing post by their post ID.

        Parameters:
        - request: The HTTP request object.
        - post_id: The ID of the post to update.

        Returns:
        - If the post exists and the data is valid, returns the updated post data.
        - If the post does not exist or the data is invalid, returns an error response.

        HTTP Methods: PUT
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

    def delete(self, request, post_id):
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
