from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils.email import send_email


@api_view(['POST'])
def send_custom_mail(request):
    """
    Send an email using the provided data.

    This endpoint allows users to send emails by providing the necessary email data in the request body.

    Request Body:
    {
        "subject": "Email Subject",
        "message": "Email Message",
        "recipient": "recipient@example.com",
        "recipient_name": "Recipient Name"
    }

    Returns:
    - 200 OK: If the email is sent successfully.
    - 400 Bad Request: If there are missing or invalid email data.
    """
    subject = request.data.get('subject')
    message = request.data.get('message')
    recipient = request.data.get('recipient')
    recipient_name = request.data.get('recipient_name')

    if not subject or not message or not recipient:
        return Response({'error': 'Missing email data'}, status=400)

    try:
        context = {"recipient_name": recipient_name, "message": message}
        send_email(recipient, subject, context)
        return Response({'message': 'Email sent successfully'}, status=200)
    except Exception as e:
        return Response({'error': 'Unable to send email: ' + str(e)}, status=400)
