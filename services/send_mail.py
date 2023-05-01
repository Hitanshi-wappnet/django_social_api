from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_mail(*args, **kwargs):

    subject = kwargs.get("subject")
    content = kwargs.get("content")
    recipient_list = kwargs.get("recipient_list")

    msg = EmailMultiAlternatives(subject, content,
                                 settings.EMAIL_HOST_USER, recipient_list)
    # msg.attach_alternative(True, "text/html")
    msg.send()
