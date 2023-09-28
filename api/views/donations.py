from functools import wraps, reduce

from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from api.models.donation import Donation
from api.serializers.donation import DonationSerializer


def admin_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if getattr(user, "role", None) in [
            "super-admin",
            "admin",
            "finance-admin",
        ]:
            return view_func(request, *args, **kwargs)
        else:
            return Response({"message": "Administrator is not authorized"}, status=403)

    return _wrapped_view


@api_view(["GET"])
@admin_access_required
def get_donation(request, donation_id):
    """
    Retrieve details of a donation by their donation ID.

    Parameters:
    - donation_id: The ID of the donation to retrieve.

    Returns:
    - If the donation exists, returns the serialized donation data.
    - If the donation does not exist, returns an error response.
    """
    try:
        donation = Donation.objects.get(pk=donation_id)

        serializer = DonationSerializer(donation)
        return Response(serializer.data)
    except Donation.DoesNotExist:
        return Response(
            {"error": "Donation not found."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def create_donation(request):
    """
    Create a new donation.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the donation is created successfully, returns the generated token.
    - If the donation data is invalid, returns an error response.

    HTTP Methods: DONATION
    """
    serializer = DonationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def update_donation(request, donation_id):
    """
    Update an existing donation by their donation ID.

    Parameters:
    - request: The HTTP request object.
    - donation_id: The ID of the donation to update.

    Returns:
    - If the donation exists and the data is valid, returns the updated donation data.
    - If the donation does not exist or the data is invalid, returns an error response.

    HTTP Methods: PATCH
    """
    try:
        donation = Donation.objects.get(pk=donation_id)
    except Donation.DoesNotExist:
        return Response(
            {"error": "Donation not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = DonationSerializer(donation, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@admin_access_required
def delete_donation(request, donation_id):
    """
    Delete an existing donation by their donation ID.

    Parameters:
    - request: The HTTP request object.
    - donation_id: The ID of the donation to delete.

    Returns:
    - If the donation exists, deletes the donation and returns a success response.
    - If the donation does not exist, returns an error response.

    HTTP Methods: DELETE
    """
    try:
        donation = Donation.objects.get(pk=donation_id)
    except Donation.DoesNotExist:
        return Response(
            {"error": "Donation not found."}, status=status.HTTP_404_NOT_FOUND
        )

    donation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def search_donations(request):
    query = get_donations_query(request.data)

    offset = get_offset(request.data["page"], request.data["limit"])

    keyword = request.data.get("keyword")
    keyword_search = None

    if keyword:
        keywords = keyword.split()  # Split keyword into individual words
        keyword_queries = [
            Q(first_name__icontains=k)
            | Q(last_name__icontains=k)
            | Q(phone_number__icontains=k)
            | Q(company__icontains=k)
            | Q(invoice_number__icontains=k)
            for k in keywords
        ]

        keyword_search = reduce(lambda x, y: x | y, keyword_queries)

    if keyword_search:
        data = Donation.objects.filter(keyword_search, **query).order_by("-created_at")
    else:
        data = Donation.objects.filter(**query).order_by("-created_at")

    paginator = PageNumberPagination()
    paginator.page_size = request.data["limit"]
    paginated_posts = paginator.paginate_queryset(data, request)
    post_serializer = DonationSerializer(paginated_posts, many=True)

    return paginator.get_paginated_response(post_serializer.data)


def get_donations_query(data):
    query = {}

    if data["status"]:
        query["status"] = data["status"]

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
