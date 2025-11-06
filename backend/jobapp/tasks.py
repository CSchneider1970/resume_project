from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_resume_created_email(user_email):
    send_mail(
        subject='Successfully created your resume',
        message='I am using an old, no longer used, free email service for this test.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )
