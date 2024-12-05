from rest_framework import serializers
from .models import StudentProfile, TeacherProfile, NonTeachingStaffProfile, Admin
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'email', 'username', 'first_name',
                  'last_name', 'is_active', 'is_staff', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Admin.objects.create_user(**validated_data)
        return user


class BaseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # Will be overridden in subclasses
        fields = []   # Will be overridden in subclasses

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        return value


class StudentProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ['id']

    def validate_date_of_admission(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(
                "Date of admission cannot be in the future")
        return value


class TeacherProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = TeacherProfile
        fields = '__all__'
        read_only_fields = ['id']

    def validate_date_of_employment(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(
                "Date of employment cannot be in the future")
        return value


class NonTeachingStaffProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = NonTeachingStaffProfile
        fields = '__all__'
        read_only_fields = ['id']

    def validate_date_of_employment(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(
                "Date of employment cannot be in the future")
        return value
