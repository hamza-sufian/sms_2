from django.contrib import admin
from .models import User, Role, StudentProfile, TeacherProfile, OTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'email_verified')
    search_fields = ('username', 'email')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'program', 'date_of_admission')
    search_fields = ('user__username', 'program')

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject_taught', 'date_of_employment')
    search_fields = ('user__username', 'subject_taught')

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'expiration_time')
    search_fields = ('user__username', 'code')
