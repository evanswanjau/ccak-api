"""
This file handles all view functions
"""
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models.socialpost import SocialPost
from api.serializers.socialpost import SocialPostSerializer


@api_view(['GET'])
def socialposts(request):
    data = SocialPost.objects.all()
    serializer = SocialPostSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def mysocialposts(request):
    data = SocialPost.objects.get(created_by=0)
    serializer = SocialPostSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def socialpost(request, social_post_id=None):
    if request.method == 'POST':
        serializer = SocialPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        try:
            data = SocialPost.objects.get(pk=social_post_id)
        except SocialPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = SocialPostSerializer(data)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = SocialPostSerializer(data, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            serializer = SocialPostSerializer(data)
            data.delete()
            return Response(serializer.data)


