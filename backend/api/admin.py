from django.contrib import admin
from .models import StudentProfile, TeacherProfile, NonTeachingStaffProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'level', 'program', 'intake')

    def get_username(self, obj):
        return obj.username
    get_username.short_description = 'Username'


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'subject_taught', 'department')

    def get_username(self, obj):
        return obj.username
    get_username.short_description = 'Username'


@admin.register(NonTeachingStaffProfile)
class NonTeachingStaffProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'position', 'department')

    def get_username(self, obj):
        return obj.username
    get_username.short_description = 'Username'
