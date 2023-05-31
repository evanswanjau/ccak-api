from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.models.subscriber import Subscriber
from api.serializers.subscriber import SubscriberSerializer


class SubscriberView(APIView):
    """
    API endpoint for managing subscribers.

    Methods:
    - GET: Get all subscribers.
    - POST: Create a new subscriber.
    - DELETE: Remove a subscriber.
    """

    def get(self, request):
        """
        Get all subscribers.

        Method: GET
        Parameters: None
        Returns: A list of all subscribers on the mailing list.
        """
        subscribers = Subscriber.objects.all()
        serializer = SubscriberSerializer(subscribers, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new subscriber.

        Method: POST
        Parameters:
            - email (str): The email address of the subscriber.
        Returns: The details of the created subscriber if successful, or error messages if validation fails.
        """
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subscriber_id):
        """
        Remove a subscriber.

        Method: DELETE
        Parameters:
            - pk (int): The ID of the subscriber to be removed.
        Returns: No content if the subscriber is successfully deleted, or a 404 error if the subscriber does not exist.
        """
        try:
            subscriber = Subscriber.objects.get(pk=subscriber_id)
            subscriber.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subscriber.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
