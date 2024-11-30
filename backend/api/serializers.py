from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile, TeacherProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'contact',
            'date_of_birth',
            'address',
            'nationality',
            'government_id',
            'email_verified',
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        # Create a user with the provided data
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'level',
            'program',
            'intake',
            'date_of_admission',
            'tuition_fee',
            'balance',
            'remarks',
            'imageUrl',
            'amount_due',
            'medical_forms',
            'admission_letter',
            'payment_method',
            'payment_status',
            'payment_date',
        ]

    def create(self, validated_data):
        # Nested user creation
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        student_profile = StudentProfile.objects.create(user=user, **validated_data)
        return student_profile


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TeacherProfile
        fields = [
            'id',
            'user',
            'subject_taught',
            'date_of_employment',
            'college_degree',
            'teachers_in_the_same_program',
            'image',
        ]

    def create(self, validated_data):
        # Nested user creation
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        teacher_profile = TeacherProfile.objects.create(user=user, **validated_data)
        return teacher_profile
