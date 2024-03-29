import os
from functools import wraps

from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.models.administrator import Administrator
from api.serializers.administrator import AdministratorSerializer
from api.utils.email import send_email
from dotenv import load_dotenv

load_dotenv()


def admin_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        administrator_id = kwargs.get("administrator_id")

        if (
            getattr(user, "role", None) == "super-admin"
            or getattr(user, "id", None) == administrator_id
        ):
            return view_func(request, *args, **kwargs)
        else:
            return Response({"message": "Administrator is not authorized"}, status=403)

    return _wrapped_view


@api_view(["GET"])
@admin_access_required
def get_administrator(request, administrator_id):
    """
    Retrieve details of an administrator by their administrator ID.

    Parameters:
    - administrator_id: The ID of the administrator to retrieve.

    Returns:
    - If the administrator exists, returns the serialized administrator data.
    - If the administrator does not exist, returns an error response.
    """
    try:
        administrator = Administrator.objects.get(pk=administrator_id)

        author = Administrator.objects.get(pk=administrator.created_by_id)
        administrator.author = f"{author.first_name} {author.last_name}"

        serializer = AdministratorSerializer(administrator)
        return Response(serializer.data)
    except Administrator.DoesNotExist:
        return Response(
            {"error": "Administrator not found."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@admin_access_required
def get_administrators(request):
    """
    Retrieve all administrators.

    Returns:
    - Serialized data for all administrators.
    """
    administrators = Administrator.objects.all()

    for administrator in administrators:
        author = Administrator.objects.get(pk=administrator.created_by_id)
        administrator.author = f"{author.first_name} {author.last_name}"

    serializer = AdministratorSerializer(administrators, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@admin_access_required
def create_administrator(request):
    """
    Create a new administrator.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the administrator is created successfully, returns the generated token.
    - If the administrator data is invalid, returns an error response.
    """
    serializer = AdministratorSerializer(data=request.data)
    if serializer.is_valid():
        # Salt and hash the password
        password = serializer.validated_data.get("password")
        serializer.validated_data["password"] = make_password(password)

        serializer.validated_data["created_by"] = request.user

        administrator = serializer.save()
        send_welcome_email(administrator, password)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@admin_access_required
def update_administrator(request, administrator_id):
    """
    Update an existing administrator by their administrator ID.

    Parameters:
    - request: The HTTP request object.
    - administrator_id: The ID of the administrator to update.

    Returns:
    - If the administrator exists and the data is valid, returns the updated administrator data.
    - If the administrator does not exist or the data is invalid, returns an error response.
    """
    try:
        administrator = Administrator.objects.get(pk=administrator_id)
    except Administrator.DoesNotExist:
        return Response(
            {"error": "Administrator not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = AdministratorSerializer(administrator, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@admin_access_required
def delete_administrator(request, administrator_id):
    """
    Delete an existing administrator by their administrator ID.

    Parameters:
    - request: The HTTP request object.
    - administrator_id: The ID of the administrator to delete.

    Returns:
    - If the administrator exists, deletes the administrator and returns a success response.
    - If the administrator does not exist, returns an error response.
    """
    try:
        administrator = Administrator.objects.get(pk=administrator_id)
    except Administrator.DoesNotExist:
        return Response(
            {"error": "Administrator not found."}, status=status.HTTP_404_NOT_FOUND
        )

    administrator.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def send_welcome_email(administrator, password):
    """
    Sends a welcome email to the administrator.

    Args:
        administrator (Administrator): The administrator object.
        password (password): The administrator password.
    Returns:
        dict: The response from the send_email function.
    """
    subject = "Welcome to The CCAK CMS Portal"
    context = {
        "recipient_name": administrator.first_name,
        "email": administrator.email,
        "password": password,
        "url": os.getenv("PORTAL_URL"),
    }
    return send_email(administrator.email, subject, context, "admin_welcome_email.html")
