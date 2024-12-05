import datetime
from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from enum import Enum

# Role Enum


class RoleEnum(Enum):
    ADMIN = "Admin"
    STUDENT = "Student"
    TEACHING_STAFF = "Teaching Staff"
    NON_TEACHING_STAFF = "Non-Teaching Staff"

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]


# Base User Manager
class CustomAdminManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


# Admin Model
class Admin(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=now)

    objects = CustomAdminManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


# Base Profile Model
class BaseProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20, choices=RoleEnum.choices())
    contact = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    government_id = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="uploads/profile_pictures/", null=True, blank=True
    )

    class Meta:
        abstract = True


# Student Profile
class StudentProfile(BaseProfile):
    level = models.CharField(max_length=20, null=True, blank=True)
    program = models.CharField(max_length=100, null=True, blank=True)
    intake = models.CharField(max_length=50, null=True, blank=True)
    date_of_admission = models.DateField(null=True, blank=True, default=now)
    tuition_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    remarks = models.TextField(null=True, blank=True)
    medical_forms = models.FileField(
        upload_to="uploads/medical_forms/", null=True, blank=True)
    admission_letter = models.FileField(
        upload_to="uploads/admission_letters/", null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    payment_status = models.CharField(max_length=50, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    amount_due = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    def __str__(self):
        return f"Student Profile: {self.username}"


# Teacher Profile
class TeacherProfile(BaseProfile):
    subject_taught = models.CharField(max_length=100, null=False, blank=False)
    department = models.CharField(max_length=100, null=True, blank=True)
    date_of_employment = models.DateField(default=now)
    college_degree = models.CharField(max_length=100, null=True, blank=True)
    teachers_in_the_same_program = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Teacher Profile: {self.username}"

    def save(self, *args, **kwargs):
        print(f"Saving subject_taught: {self.subject_taught}")  # Debugging
        super().save(*args, **kwargs)


# Non-Teaching Staff Profile
class NonTeachingStaffProfile(BaseProfile):
    position = models.CharField(max_length=100)
    date_of_employment = models.DateField(default=now)
    department = models.CharField(max_length=100, null=True, blank=True)
    college_degree = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Non-Teaching Staff Profile: {self.username}"


# OTP Model
class OTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"OTP for {self.email}: {self.otp}"

    def is_valid(self):
        expiry_time = self.created_at + datetime.timedelta(minutes=10)
        return now() < expiry_time
