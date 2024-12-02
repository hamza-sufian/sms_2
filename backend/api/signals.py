from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile, TeacherProfile, NonTeachingStaffProfile
from django.utils import timezone


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'STUDENT':
            StudentProfile.objects.create(
                user=instance,
                level="Freshman",
                program="Computer Science",
                tuition_fee=10000.00,
                date_of_admission=timezone.now().date(),
                intake=f"{timezone.now().year}-{timezone.now().strftime('%B')}",
            )
        elif instance.role == 'TEACHING_STAFF':
            TeacherProfile.objects.create(
                user=instance,
                department="General",
                date_of_employment=timezone.now().date(),
                subject_taught="Not Assigned",
            )
        elif instance.role == 'NON_TEACHING_STAFF':
            NonTeachingStaffProfile.objects.create(
                user=instance,
                department="Administration",
                date_of_employment=timezone.now().date(),
                position="Not Assigned",
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'STUDENT':
        if hasattr(instance, 'student_profile'):
            instance.student_profile.save()
    elif instance.role == 'TEACHING_STAFF':
        if hasattr(instance, 'teacher_profile'):
            instance.teacher_profile.save()
    elif instance.role == 'NON_TEACHING_STAFF':
        if hasattr(instance, 'non_teaching_staff_profile'):
            instance.non_teaching_staff_profile.save()
