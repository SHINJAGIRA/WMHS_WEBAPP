import logging
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Subscriber, Blog

logger = logging.getLogger(__name__)

@shared_task
def send_new_blog_email(blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
        subscribers = Subscriber.objects.all()
        recipient_list = [subscriber.email for subscriber in subscribers]
        subject = f"New Blog Post: {blog.title}"
        html_content = render_to_string('main/email/email.html', {'blog': blog})
        
        email = EmailMultiAlternatives(
            subject,
            '',
            'tennodes10@gmail.com',
            recipient_list
        )
        email.attach_alternative(html_content, 'text/html')
        if blog.attachent:
            email.attach_file(blog.attachent.path)
        
        email.send()
        logger.debug("Email sent successfully to %d recipients", len(recipient_list))
        
        return 'email_sent', blog_id, len(recipient_list)
    
    except Blog.DoesNotExist:
        logger.error("Blog with id %d does not exist", blog_id)
        return 'blog_not_found', blog_id
    except Exception as e:
        logger.error("An error occurred while sending email: %s", e)
        raise
