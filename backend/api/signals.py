from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile, TeacherProfile, NonTeachingStaffProfile
from django.utils import timezone


@receiver(post_save, sender=StudentProfile)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        update_fields = []

        # Only set date_of_admission if it's not already set
        if not instance.date_of_admission:
            instance.date_of_admission = timezone.now().date()
            update_fields.append('date_of_admission')

        # Only set intake if it's not already set
        if not instance.intake:
            instance.intake = f"{timezone.now().year}-{timezone.now().strftime('%B')}"
            update_fields.append('intake')

        # Only set tuition_fee if it's not already set
        if instance.tuition_fee is None:
            instance.tuition_fee = 10000.00  # Default value, can be modified as needed
            update_fields.append('tuition_fee')

        if update_fields:
            instance.save(update_fields=update_fields)


@receiver(post_save, sender=TeacherProfile)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        update_fields = []

        if not instance.subject_taught:
            instance.subject_taught = "Not Assigned"
            update_fields.append('subject_taught')

        # Only set date_of_employment if it's not already set
        if not instance.date_of_employment:
            instance.date_of_employment = timezone.now().date()
            update_fields.append('date_of_employment')

        if update_fields:
            instance.save(update_fields=update_fields)


@receiver(post_save, sender=NonTeachingStaffProfile)
def create_non_teaching_staff_profile(sender, instance, created, **kwargs):
    if created:
        update_fields = []

        if not instance.department:
            instance.department = "Not Assigned"
            update_fields.append('department')

        # Only set date_of_employment if it's not already set
        if not instance.date_of_employment:
            instance.date_of_employment = timezone.now().date()
            update_fields.append('date_of_employment')

        if update_fields:
            instance.save(update_fields=update_fields)
