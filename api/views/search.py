from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.models.post import Post
from api.models.invoice import Invoice
from api.models.payment import Payment
from api.models.member import Member
from api.serializers.post import PostSerializer
from api.serializers.invoice import InvoiceSerializer
from api.serializers.payment import PaymentSerializer
from api.serializers.member import MemberSerializer
from api.serializers.search import SearchSerializer


@api_view(['POST'])
def search_posts(request):
    """
    Search view that searches for posts based on specified criteria.

    Request Method: POST

    Request Body Parameters:
        - keyword (string): The keyword to search for in post titles.
        - category (string): The category of posts to search in.
        - project_status (string): (Optional) The status of project posts to filter by.
        - technology (string): (Optional) The member technology to filter by.
        - page (integer): The page number for pagination.
        - limit (integer): The maximum number of results per page.

    Returns:
        - Response with paginated list of matching post objects.

    Algorithm:
        1. Extract the keyword, category, project_status, page, and limit from the request data.
        2. Create a search query based on the provided criteria.
        3. Perform a database query to retrieve posts matching the query.
        4. Apply pagination to the query results based on the page and limit.
        5. Serialize the paginated posts data.
        6. Return the paginated posts as a JSON response.

    Note:
        - The search query filters posts based on the keyword, category, and project status (if provided).
        - Posts are ordered by 'published' if the category is 'events', otherwise by 'event_date'.
        - The pagination is implemented using the 'page' and 'limit' parameters.
        - The response includes the paginated list of post objects.
    """
    serializer = SearchSerializer(data=request.data)
    if serializer.is_valid():
        category = request.data.get('category')

        # get search query arguments
        query = get_posts_query(request.data)
        print(query)

        # get search offset range and limit
        offset = get_offset(request.data['page'], request.data['limit'])

        if category in ["events"]:
            data = Post.objects.filter(**query, event_date__gt=datetime.today()).order_by("event_date")[
                   offset["start"]:offset["end"]]
        else:
            data = Post.objects.filter(**query).order_by("-published")[offset["start"]:offset["end"]]

        post_serializer = PostSerializer(data, many=True)
        return Response(post_serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
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
    serializer = SearchSerializer(data=request.data)
    if serializer.is_valid():
        keyword = request.data.get('keyword')
        category = request.data.get('category')
        table = request.data.get('table')
        technology = request.data.get('technology')

        # get search query arguments
        if request.data.get('table') == 'members':
            query = get_posts_query(request.data)

        # get search offset range and limit
        offset = get_offset(request.data['page'], request.data['limit'])

        # initiate search
        data = Member.objects.filter(**query).order_by('company')[offset["start"]:offset["end"]]

        member_serializer = MemberSerializer(data, many=True)
        return Response(member_serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def search_invoices(request):
    """
    Search and retrieve a paginated list of invoices based on the provided search criteria.

    Args:
        request (Request): The HTTP POST request containing the search parameters.

    Returns:
        Response: A Response object containing the serialized data of the matching invoices.

    Raises:
        - KeyError: If the 'page' or 'limit' keys are not present in the request data.
        - Exception: If there is an error while processing the search or serialization.
    """
    query = get_invoices_query(request.data)

    offset = get_offset(request.data['page'], request.data['limit'])
    data = Invoice.objects.filter(**query).order_by("-created_at")[offset["start"]:offset["end"]]

    for invoice in data:
        invoice = payment_details(invoice)

    serializer = InvoiceSerializer(data, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def search_payments(request):
    query = get_payments_query(request.data)

    offset = get_offset(request.data['page'], request.data['limit'])
    data = Payment.objects.filter(**query).order_by("-created_at")[offset["start"]:offset["end"]]

    serializer = PaymentSerializer(data, many=True)

    return Response(serializer.data)


def get_posts_query(data):
    query = {}

    if data['keyword']:
        query["title__contains"] = data['keyword']

    if data['category']:
        query["category"] = data['category']

    if data['category'] == "projects" and data['project_status']:
        query["project_status"] = data['project_status']

    if data['access']:
        query["access"] = data['access']
        if data['access'] == 'public':
            query['published__lt'] = datetime.today()

    if data['status']:
        query["status"] = data['status']

    return query


def get_invoices_query(data):
    query = {}

    if data['invoice_number']:
        query["invoice_number__contains"] = data['invoice_number']

    if data['type']:
        query["description__contains"] = data['type']

    if data['status']:
        query["status"] = data['status']

    return query


def get_payments_query(data):
    query = {}

    if data['transaction_id']:
        query["transaction_id__contains"] = data['transaction_id']

    if data['method']:
        query["method"] = data['method']

    if data['invoice_number']:
        query["invoice_number__contains"] = data['invoice_number']

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
    start = (end - limit)
    start = start + 1 if start != 0 else start

    return {"start": start, "end": end}


def payment_details(invoice):
    """
    Calculates the payment details for an invoice.

    Args:
        invoice (Invoice): The invoice object for which to calculate the payment details.

    Returns:
        Invoice: The updated invoice object with total amount, paid amount, and balance calculated.
    """
    total_amount = 0
    paid_amount = 0

    for item in invoice.items:
        total_amount += item['quantity'] * item['unit_price']

    invoice.total_amount = total_amount

    payments = Payment.objects.filter(invoice_number=invoice.invoice_number)
    for payment in payments:
        paid_amount += payment.amount

    invoice.paid_amount = paid_amount
    invoice.balance = total_amount - paid_amount

    return invoice
