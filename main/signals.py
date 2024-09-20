from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .tasks import send_new_blog_email
from .models import *

@receiver(post_save,sender=Blog)
def send_new_blog_mail(sender,instance,created,**kwargs):
   if created:
    send_new_blog_email.delay(instance.id)