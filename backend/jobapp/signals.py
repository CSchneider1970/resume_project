from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Resume
from .tasks import send_resume_created_email

@receiver(post_save, sender=Resume)
def resume_created_handler(sender, instance, created, **kwargs):
    if created and instance.user and instance.user.email:
        send_resume_created_email.delay(instance.user.email)
