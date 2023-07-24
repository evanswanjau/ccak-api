import base64
import os

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from imagekitio.models.ListAndSearchFileRequestOptions import ListAndSearchFileRequestOptions
from api.serializers.imagekit import ImagekitSerializer
from dotenv import load_dotenv

load_dotenv()

imagekit = ImageKit(
    private_key=os.getenv('IMAGEKIT_PRIVATE_KEY'),
    public_key=os.getenv('IMAGEKIT_PUBLIC_KEY'),
    url_endpoint=os.getenv('IMAGEKIT_URL_ENDPOINT')
)


@api_view(['GET'])
def auth(request):
    """
    Acquires ImageKit method.

    This method retrieves the necessary configuration files and authentication parameters
    from ImageKit to enable secure interactions with the ImageKit service.

    Returns:
        JsonResponse: JSON response containing the ImageKit authentication parameters.
    """
    response = imagekit.get_authentication_parameters()
    return JsonResponse(response)


@api_view(['POST'])
def upload_file(request):
    """
       Uploads a file to an external image storage service using Imagekit.

       Args:
           request (Request): The HTTP request object containing the file and related information.

       Returns:
           Response: The HTTP response containing the serialized data of the uploaded file.

       Raises:
           Exception: If an error occurs during the file upload process.
    """
    try:
        response = imagekit.upload_file(
            file=base64.b64encode(request.data.get('file').file.read()),
            file_name=request.data.get('file_name'),
            options=UploadFileRequestOptions(
                folder="/" + request.data.get('folder')
            )
        )
        serializer = ImagekitSerializer(response)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['DELETE'])
def delete_file(request):
    """
    Delete a file by name.

    Args:
        request (Request): The Django request object.

    Returns:
        Response: The Django response object.

    Raises:
        Exception: If an error occurs during the deletion process.
    """
    try:
        response = imagekit.delete_file(file_id=request.data.get("file_id"))

        if response.response_metadata.http_status_code == 204:
            return Response({'message': 'Image deleted successfully'})
        else:
            return Response({'error': 'Failed to delete image'})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
