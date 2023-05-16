"""
This file handles all view functions
"""
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Post
from ..serializers import PostSerializer


@api_view(['GET'])
def posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def post(request, id=None):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PostSerializer(post)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = PostSerializer(post, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            serializer = PostSerializer(post)
            post.delete()
            return Response(serializer.data)


