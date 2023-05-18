"""
This file handles all view functions
"""
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models.post import Post
from api.serializers.post import PostSerializer


@api_view(['GET'])
def posts(request):
    data = Post.objects.order_by("created_at").all()
    serializer = PostSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def post(request, post_id=None):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        try:
            data = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PostSerializer(data)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = PostSerializer(data, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            serializer = PostSerializer(data)
            data.delete()
            return Response(serializer.data)


@api_view(['GET'])
def search_posts(request, keyword, category, limit):
    if keyword == "all":
        data = Post.objects.filter(category=category)[:limit]
    else:
        data = Post.objects.filter(title__contains=keyword, category=category)

    serializer = PostSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)
