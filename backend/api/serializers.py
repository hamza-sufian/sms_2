from rest_framework import serializers
from .models import User, StudentProfile, TeacherProfile, NonTeachingStaffProfile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'role', 'contact',
                  'date_of_birth', 'address', 'nationality', 'government_id', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}


class BaseProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    name = serializers.CharField(source='user.name', required=False)
    role = serializers.CharField(source='user.role', required=False)
    contact = serializers.CharField(source='user.contact', required=False)
    date_of_birth = serializers.DateField(
        source='user.date_of_birth', required=False)
    address = serializers.CharField(source='user.address', required=False)
    nationality = serializers.CharField(
        source='user.nationality', required=False)
    government_id = serializers.CharField(
        source='user.government_id', required=False)
    profile_picture = serializers.ImageField(
        source='user.profile_picture', required=False)

    class Meta:
        model = None
        fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = UserSerializer(instance.user).data
        for field in user_representation:
            if field in representation:
                representation[field] = user_representation[field]
        return representation

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        return value


class StudentProfileSerializer(BaseProfileSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    name = serializers.CharField(source='user.name', required=False)
    role = serializers.CharField(source='user.role', required=False)
    contact = serializers.CharField(source='user.contact', required=False)
    date_of_birth = serializers.DateField(
        source='user.date_of_birth', required=False)
    address = serializers.CharField(source='user.address', required=False)
    nationality = serializers.CharField(
        source='user.nationality', required=False)
    government_id = serializers.CharField(
        source='user.government_id', required=False)
    profile_picture = serializers.ImageField(
        source='user.profile_picture', required=False
    )

    class Meta:
        model = StudentProfile
        fields = BaseProfileSerializer.Meta.fields + ['id', 'level', 'program', 'intake', 'date_of_admission',
                                                      'tuition_fee', 'balance', 'remarks', 'medical_forms', 'admission_letter',
                                                      'payment_method', 'payment_status', 'payment_date', 'amount_due']

    def validate_date_of_admission(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(
                "Date of admission cannot be in the future")
        return value


class TeacherProfileSerializer(BaseProfileSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    name = serializers.CharField(source='user.name', required=False)
    role = serializers.CharField(source='user.role', required=False)
    contact = serializers.CharField(source='user.contact', required=False)
    date_of_birth = serializers.DateField(
        source='user.date_of_birth', required=False)
    address = serializers.CharField(source='user.address', required=False)
    nationality = serializers.CharField(
        source='user.nationality', required=False)
    government_id = serializers.CharField(
        source='user.government_id', required=False)
    profile_picture = serializers.ImageField(
        source='user.profile_picture', required=False
    )

    class Meta:
        model = TeacherProfile
        fields = BaseProfileSerializer.Meta.fields + ['id', 'subject_taught', 'department', 'date_of_employment',
                                                      'college_degree', 'teachers_in_the_same_program']

    def validate_date_of_employment(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(
                "Date of employment cannot be in the future")
        return value


class NonTeachingStaffProfileSerializer(BaseProfileSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    name = serializers.CharField(source='user.name', required=False)
    role = serializers.CharField(source='user.role', required=False)
    contact = serializers.CharField(source='user.contact', required=False)
    date_of_birth = serializers.DateField(
        source='user.date_of_birth', required=False)
    address = serializers.CharField(source='user.address', required=False)
    nationality = serializers.CharField(
        source='user.nationality', required=False)
    government_id = serializers.CharField(
        source='user.government_id', required=False)
    profile_picture = serializers.ImageField(
        source='user.profile_picture', required=False
    )

    class Meta:
        model = NonTeachingStaffProfile
        fields = BaseProfileSerializer.Meta.fields + \
            ['id', 'position', 'date_of_employment', 'department', 'college_degree']

    def validate_date_of_employment(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(
                "Date of employment cannot be in the future")
        return value
