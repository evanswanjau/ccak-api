from functools import wraps

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models.subscriber import Subscriber
from api.serializers.subscriber import SubscriberSerializer
from api.utils.email import send_email


def admin_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        print(user.__dict__)
        print(getattr(user, "role", None))

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
@admin_access_required
def get_subscribers(request):
    """
    Get all subscribers.

    Method: GET
    Parameters: None
    Returns: A list of all subscribers on the mailing list.
    """
    if getattr(request.user, "role", None) not in [
        "super-admin",
        "admin",
        "content-admin",
    ]:
        return Response({"message": "Administrator is not authorized"}, status=403)

    subscribers = Subscriber.objects.all()

    serializer = SubscriberSerializer(subscribers, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_subscriber(request):
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

        # Send welcome email to subscriber
        send_welcome_email(request.data.get("email"))

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@admin_access_required
def delete_subscriber(request, subscriber_id):
    """
    Remove a subscriber.

    Method: DELETE
    Parameters:
        - subscriber_id (int): The ID of the subscriber to be removed.
    Returns: No content if the subscriber is successfully deleted, or a 404 error if the subscriber does not exist.
    """
    if getattr(request.user, "role", None) not in [
        "super-admin",
        "admin",
        "content-admin",
    ]:
        return Response({"message": "Administrator is not authorized"}, status=403)

    try:
        subscriber = Subscriber.objects.get(pk=subscriber_id)
        subscriber.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Subscriber.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def send_welcome_email(email):
    """
    Sends a welcome subscriber email to the subscriber.

    Args:
        email (Member): The subscriber email.

    Returns:
        dict: The response from the send_email function.
    """
    subject = "You Have Been Subscribed"
    context = {"recipient_name": "subscriber"}

    send_email(email, subject, context, "subscriber_email.html")
