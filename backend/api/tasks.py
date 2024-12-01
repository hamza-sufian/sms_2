from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@shared_task
def send_otp_email(user_id, otp_code):
    user = User.objects.get(id=user_id)
    subject = "Your Admin OTP Code"
    message = f"""
    Hello {user.username},

    Your OTP code for admin login is: {otp_code}
    It will expire in 10 minutes.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])