from django.conf import settings
from django.core.mail import send_mail
from email.utils import formataddr


def send_email(recipient, subject, message):
    """
    Sends an email to the specified recipient.

    Parameters:
    - recipient: The email address of the recipient.
    - subject: The subject of the email.
    - message: The content of the email.

    Returns:
    - True if the email was sent successfully, False otherwise.
    """
    try:
        from_email = formataddr((settings.EMAIL_HOST_NAME, settings.EMAIL_HOST_USER))
        send_mail(subject, message, from_email, [recipient])
        return True
    except Exception as e:
        # Handle any exceptions that occurred during email sending
        print(f"Error sending email: {e}")
        return False
