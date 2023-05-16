"""
This file handles member view functions
"""
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models.member import Member
from api.serializers.member import MemberSerializer


@api_view(['GET'])
def members(request):
    data = Member.objects.all()
    serializer = MemberSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def member(request, member_id=None):
    if request.method == 'POST':
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        try:
            data = Member.objects.get(pk=member_id)
            print(data)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = MemberSerializer(data)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = MemberSerializer(data, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            serializer = MemberSerializer(data)
            data.delete()
            return Response(serializer.data)


