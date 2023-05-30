from django.http import JsonResponse
from rest_framework.decorators import api_view
from api.models.post import Post
from api.serializers.post import PostSerializer
from api.serializers.search import SearchSerializer


@api_view(['POST'])
def search(request):
    """
    Search view that searches for all the posts based on values given
    """
    keyword = request.data['keyword']
    category = request.data['category']

    # get search query arguments
    query = get_query(keyword, category, request.data['project_status'])

    # get search offset range and limit
    offset = get_offset(request.data['page'], request.data['limit'])

    # initiate search
    data = Post.objects.filter(**query).order_by('published' if category == "events" else 'event_date')[
           offset["start"]:offset["end"]]

    # save search
    save_search(request.data)

    serializer = PostSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_query(keyword, category, project_status):
    """
    Function that gets the search query status
    """
    query = {"category": category, "access": "public", "status": "published"}

    if keyword != "":
        query["title__contains"] = keyword
    if category == "projects" and project_status != "":
        query["project_status"] = project_status
    if category == "":
        del query["category"]

    return query


def get_offset(page, limit):
    """
    Function that calculates the pagination range
    """
    end = limit * page
    start = (end - limit)

    if start != 0:
        start += 1

    return {"start": start, "end": end}


def save_search(data):
    """
    Function that stores the search parameters
    """
    serialized_search = SearchSerializer(data=data)
    if serialized_search.is_valid():
        serialized_search.save()
        print("valid", True)
        return True
    else:
        print("valid", False)
        return False
