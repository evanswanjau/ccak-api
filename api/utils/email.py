from django.conf import settings
from django.core.mail import send_mail
from email.utils import formataddr
from django.template.loader import render_to_string


def send_email(recipient, subject, context, template="default_email.html"):
    """
    Sends an email to the specified recipient.

    Args:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        context (dict): The context data to render the email template.
        template (str): The name of the email template to use. Default is "default_email.html".

    Returns:
        dict: The response from the send_mail function.

    Raises:
        Exception: If there is an error while sending the email.
    """
    email_content = render_to_string(f'emails/{template}', context)

    from_email = formataddr((settings.EMAIL_HOST_NAME, settings.EMAIL_HOST_USER))

    return send_mail(subject, None, from_email, [recipient], html_message=email_content)
