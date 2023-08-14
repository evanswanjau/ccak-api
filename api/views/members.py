import os

from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models.member import Member
from api.serializers.member import MemberSerializer
from api.utils.email import send_email
from dotenv import load_dotenv

load_dotenv()


@api_view(["GET"])
def get_member(request, member_id):
    """
    Retrieve details of a member by their member ID.

    Parameters:
    - member_id: The ID of the member to retrieve.

    Returns:
    - If the member exists, returns the serialized member data.
    - If the member does not exist, returns an error response.
    """
    try:
        member = Member.objects.get(pk=member_id)
        serializer = MemberSerializer(member)
        return Response(serializer.data)
    except Member.DoesNotExist:
        return Response(
            {"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def get_members(request):
    """
    Retrieve all members.

    Returns:
    - Serialized data for all members.
    """
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_member(request):
    """
    Create a new member.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the member is created successfully, returns the generated token.
    - If the member data is invalid, returns an error response.

    HTTP Methods: POST
    """
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data.get("password")
        serializer.validated_data["password"] = make_password(password)
        member = serializer.save()
        token = generate_token(member)
        data_from = request.data.get("data_from")
        if data_from == "portal":
            send_welcome_email(member, password)
        elif data_from == "website":
            send_verification_email(member, token.get("access"))
        return Response({"token": token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def update_member(request, member_id):
    """
    Update an existing member by their member ID.

    Parameters:
    - request: The HTTP request object.
    - member_id: The ID of the member to update.

    Returns:
    - If the member exists and the data is valid, returns the updated member data.
    - If the member does not exist or the data is invalid, returns an error response.

    HTTP Methods: PATCH
    """
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        return Response(
            {"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = MemberSerializer(member, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_member(request, member_id):
    """
    Delete an existing member by their member ID.

    Parameters:
    - request: The HTTP request object.
    - member_id: The ID of the member to delete.

    Returns:
    - If the member exists, deletes the member and returns a success response.
    - If the member does not exist, returns an error response.

    HTTP Methods: DELETE
    """
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        return Response(
            {"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND
        )

    member.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def generate_token(user):
    """
    Generate an authentication token for a member.

    Parameters:
    - member: The member object.

    Returns:
    - The generated token object.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def send_verification_email(member, token):
    """
    Sends a verification email to the member.

    Args:
        member (Member): The member object.
        token (str): The verification token for email verification.

    Returns:
        dict: The response from the send_email function.
    """
    subject = "Welcome to The Clean Cooking Association Kenya"
    context = {
        "recipient_name": member.first_name,
        "token": token,
        "url": os.getenv("FRONTEND_URL"),
    }
    return send_email(member.email, subject, context, "welcome_email.html")


def send_welcome_email(member, password):
    """
    Sends a welcome email to the member.

    Args:
        member (Member): The member object.
        password (str): The unsalted password

    Returns:
        dict: The response from the send_email function.
    """
    subject = "Welcome to The Clean Cooking Association Kenya. Your Account is Ready!"
    context = {
        "recipient_name": member.first_name,
        "email": member.email,
        "password": password,
        "url": os.getenv("FRONTEND_URL"),
    }
    return send_email(member.email, subject, context, "member_welcome_email.html")


@api_view(["POST"])
def search_members(request):
    """
    Search members based on specified criteria.

    Request Method: POST

    Request Body Parameters:
        - keyword (str): The keyword to search for in member information.
        - category (str): The category of members to search in.
        - technology (str): (Optional) The technology to filter members by.
        - page (int): The page number for pagination.
        - limit (int): The maximum number of results per page.

    Returns:
        - Response with paginated list of matching member objects.

    Algorithm:
        1. Validate the serializer with the request data.
        2. Extract the keyword, category, technology, page, and limit from the request data.
        3. Create a search query based on the provided criteria.
        4. Perform a database query to retrieve members matching the query.
        5. Apply pagination to the query results based on the page and limit.
        6. Serialize the paginated member data.
        7. Return the paginated members as a JSON response.

    Note:
        - The search query filters members based on the keyword, category, and technology (if provided).
        - Members are ordered by 'company'.
        - The pagination is implemented using the 'page' and 'limit' parameters.
        - The response includes the paginated list of member objects.
    """
    query = get_members_query(request.data)

    offset = get_offset(request.data["page"], request.data["limit"])
    data = Member.objects.filter(**query).order_by("company")[
        offset["start"] : offset["end"]
    ]

    member_serializer = MemberSerializer(data, many=True)
    return Response(member_serializer.data)


def get_members_query(data):
    query = {}

    if data["keyword"]:
        query["company__contains"] = data["keyword"]

    if data["technology"]:
        query["technology"] = data["technology"]

    if data["registration_status"]:
        query["registration_status"] = data["registration_status"]

    if data["subscription_status"]:
        query["subscription_status"] = data["subscription_status"]

    return query


def get_offset(page, limit):
    """
    Calculate the pagination range.

    Args:
        page (int): The current page number.
        limit (int): The maximum number of items per page.

    Returns:
        dict: A dictionary containing the start and end offsets for pagination.
    """
    end = limit * page
    start = end - limit
    start = start + 1 if start != 0 else start

    return {"start": start, "end": end}
