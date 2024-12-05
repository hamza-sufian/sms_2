from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import StudentProfile, TeacherProfile, NonTeachingStaffProfile


@shared_task
def send_otp_email(profile_id, otp_code, profile_type):
    """
    Sends an OTP email to the user based on the profile type.

    Parameters:
    - profile_id: ID of the profile (StudentProfile, TeacherProfile, NonTeachingStaffProfile)
    - otp_code: OTP code to be sent
    - profile_type: Type of the profile (either 'student', 'teacher', or 'non_teaching_staff')
    """
    # Fetch the profile based on the type and ID provided
    if profile_type == 'student':
        profile = StudentProfile.objects.get(id=profile_id)
    elif profile_type == 'teacher':
        profile = TeacherProfile.objects.get(id=profile_id)
    elif profile_type == 'non_teaching_staff':
        profile = NonTeachingStaffProfile.objects.get(id=profile_id)
    else:
        raise ValueError("Invalid profile type")

    # Construct the email details
    subject = "Your OTP Code"
    message = f"""
    Hello {profile.username},  # Assumes `username` field exists in each profile model

    Your OTP code for login is: {otp_code}
    It will expire in 10 minutes.
    """

    # Send the email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [profile.email])
