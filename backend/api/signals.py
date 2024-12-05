from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile, TeacherProfile, NonTeachingStaffProfile
from django.utils import timezone

# Signal to create a profile when a new instance is created


@receiver(post_save, sender=StudentProfile)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        # Initialize any additional attributes or setup needed for the student profile
        instance.date_of_admission = timezone.now().date()
        instance.intake = f"{timezone.now().year}-{timezone.now().strftime('%B')}"
        instance.tuition_fee = 10000.00  # Default value, can be modified as needed
        instance.save()


@receiver(post_save, sender=TeacherProfile)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        # Initialize any additional attributes or setup needed for the teacher profile
        instance.date_of_employment = timezone.now().date()
        # Default value, can be modified as needed
        instance.subject_taught = "Not Assigned"
        instance.save()


@receiver(post_save, sender=NonTeachingStaffProfile)
def create_non_teaching_staff_profile(sender, instance, created, **kwargs):
    if created:
        # Initialize any additional attributes or setup needed for the non-teaching staff profile
        instance.date_of_employment = timezone.now().date()
        instance.position = "Not Assigned"  # Default value, can be modified as needed
        instance.save()

# Signal to save profile if there are updates to any of the profiles


@receiver(post_save, sender=StudentProfile)
def save_student_profile(sender, instance, **kwargs):
    if hasattr(instance, 'student_profile'):
        instance.student_profile.save()


@receiver(post_save, sender=TeacherProfile)
def save_teacher_profile(sender, instance, **kwargs):
    if hasattr(instance, 'teacher_profile'):
        instance.teacher_profile.save()


@receiver(post_save, sender=NonTeachingStaffProfile)
def save_non_teaching_staff_profile(sender, instance, **kwargs):
    if hasattr(instance, 'non_teaching_staff_profile'):
        instance.non_teaching_staff_profile.save()
