import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator

# Role Model for defining user roles


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Force role to ADMIN for superusers
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STUDENT', 'Student'),
        ('TEACHER_STAFF', 'Teaching Staff'),
        ('NON_TEACHING_STAFF', 'Non-Teaching Staff'),
    ]
    name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    contact = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    government_id = models.CharField(max_length=100, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to='uploads/profile_pictures/', null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Use email as the unique login identifier
    REQUIRED_FIELDS = ['username']  # Fields required for creating a superuser

    objects = UserManager()  # Link to the custom manager

    def is_admin(self):
        return self.role == 'ADMIN'

    def save(self, *args, **kwargs):
        if not self.name and (self.first_name or self.last_name):
            self.name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else self.username

# Student Profile Model


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile")
    level = models.CharField(max_length=20, null=True, blank=True)
    program = models.CharField(max_length=100, null=True, blank=True)
    intake = models.CharField(max_length=50, null=True, blank=True)
    date_of_admission = models.DateField(null=True, blank=True)
    tuition_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    remarks = models.TextField(null=True, blank=True)
    medical_forms = models.FileField(null=True, blank=True)
    admission_letter = models.FileField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    payment_status = models.CharField(max_length=50, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    amount_due = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return f"Student Profile for {self.user.username}"

    def is_student(self):
        return self.role == 'STUDENT'


# Teacher Profile Model


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="teacher_profile")
    subject_taught = models.CharField(max_length=100)
    department = models.CharField(max_length=100, null=True, blank=True)
    date_of_employment = models.DateField(
        null=False, default=datetime.date.today)
    college_degree = models.CharField(max_length=100, null=True, blank=True)
    teachers_in_the_same_program = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Teacher Profile for {self.user.username}"

    def is_teacher(self):
        return self.role == 'TEACHING_STAFF'


class NonTeachingStaffProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="non_teaching_staff_profile")
    position = models.CharField(max_length=100)
    date_of_employment = models.DateField()
    department = models.CharField(max_length=100, null=True, blank=True)
    college_degree = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Non-Teaching Staff Profile for {self.user.username}"

    def is_non_teaching_staff(self):
        return self.role == 'NON_TEACHING_STAFF'
# OTP Model for storing OTP information


class OTP(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otp")
    code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()

    # Utility method to check if OTP is valid
    def is_valid(self):
        return now() < self.expiration_time

    def __str__(self):
        return f"OTP for {self.user.username} (expires at {self.expiration_time})"
