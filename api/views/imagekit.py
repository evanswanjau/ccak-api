"""
This view handles all imagkit endpoints (verification)
"""
import os
from django.http import JsonResponse
from imagekitio import ImageKit
from dotenv import load_dotenv
from rest_framework.decorators import api_view

load_dotenv()


@api_view(['GET'])
def auth(request):
    """
    This method acquires imagekit config files
    Acquires imagekit authorization 
    Returns security data
    """
    imagekit = ImageKit(
        private_key=os.getenv('IMAGEKIT_PRIVATE_KEY'),
        public_key=os.getenv('IMAGEKIT_PUBLIC_KEY'),
        url_endpoint=os.getenv('IMAGEKIT_URL_ENDPOINT')
    )

    response = imagekit.get_authentication_parameters()
    return JsonResponse(response)
