from django.conf import settings
from django.core.mail import send_mail
from email.utils import formataddr
from django.template.loader import render_to_string


def send_email(recipient, recipient_name, subject, message):
    """
    Sends an email to the specified recipient.

    Parameters:
    - recipient (str): The email address of the recipient.
    - recipient_name (str): The name of the recipient.
    - subject (str): The subject of the email.
    - message (str): The content of the email.

    Returns:
    - dict: The response from the send_mail function.

    Raises:
    - Exception: If there is an error while sending the email.
    """
    context = {
        'recipient_name': recipient_name,
        'message': message
    }

    email_content = render_to_string('emails/default_email.html', context)

    from_email = formataddr((settings.EMAIL_HOST_NAME, settings.EMAIL_HOST_USER))

    return send_mail(subject, None, from_email, [recipient], html_message=email_content)
