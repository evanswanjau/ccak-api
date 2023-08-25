import os

from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models.member import Member
from api.models.administrator import Administrator
from api.utils.email import send_email


@api_view(["POST"])
def member_login(request):
    """
    Authenticate a member and generate JWT tokens.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the login is successful, returns the generated tokens.
    - If the login fails, returns an error response.

    HTTP Methods: POST
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if email and password:
        member = Member.objects.filter(email=email).first()

        if member and check_password(password, member.password):
            # Generate tokens
            refresh = RefreshToken.for_user(member)
            refresh["user_type"] = "member"
            refresh.access_token.payload["user_type"] = "member"

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    else:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def administrator_login(request):
    """
    Authenticate an administrator and generate JWT tokens.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the login is successful, returns the generated tokens.
    - If the login fails, returns an error response.

    HTTP Methods: POST
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if email and password:
        administrator = Administrator.objects.filter(email=email).first()

        if administrator.status == "inactive":
            return Response(
                {"error": "Administrator has been deactivated"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if administrator and check_password(password, administrator.password):
            # Generate tokens
            refresh = RefreshToken.for_user(administrator)
            refresh["user_type"] = "admin"  # Add custom claim to the payload
            refresh.access_token.payload[
                "user_type"
            ] = "admin"  # Also add to the access token's payload

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    else:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def reset_link(request):
    """
    Reset Link API Endpoint

    This endpoint allows the user to request a password reset link.

    Parameters:
        - request (HttpRequest): The HTTP request object.

    Returns:
        Response (Response): A response containing the result of the request.
    """
    email = request.data.get("email")
    user_type = request.data.get("user_type")

    user = None
    if user_type == "administrator":
        user = Administrator.objects.filter(email=email).first()

    if user_type == "member":
        user = Member.objects.filter(email=email).first()

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    refresh["user_type"] = user_type  # Add custom claim to the payload
    refresh.access_token.payload[
        "user_type"
    ] = "admin"  # Also add to the access token's payload

    if user and user.email:
        send_reset_link_email(user, refresh.access_token)

    return Response(
        {"success": "Your email has been sent successfully"},
        status=status.HTTP_200_OK,
    )


def send_reset_link_email(user, token):
    """
    Sends a password reset link email to the user.

    Args:
        token: A secure token
        user (Member): The user object.

    Returns:
        dict: The response from the send_email function.
    """
    subject = "Reset Your CCAK Password"
    context = {
        "recipient_name": user.first_name,
        "token": token,
        "url": os.getenv("FRONTEND_URL"),
    }
    return send_email(user.email, subject, context, "reset_link_email.html")
