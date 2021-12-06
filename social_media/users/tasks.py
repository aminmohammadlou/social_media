from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_code_task(email_data):
    send_mail(**email_data,
              from_email='aminmhml@gmail.com',
              fail_silently=False)
    return None
