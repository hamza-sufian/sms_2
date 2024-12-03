from rest_framework import serializers
from .models import User, StudentProfile, TeacherProfile, NonTeachingStaffProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'role', 'contact',
                  'date_of_birth', 'address', 'nationality', 'government_id', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}


class BaseProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = '__all__'

    def to_representation(self, instance):
        """Customize how the nested user is represented in the response."""
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        return self.Meta.model.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = {}
        for field in ['username', 'email',  'name', 'role', 'contact', 'date_of_birth', 'address', 'nationality', 'government_id', 'profile_picture']:  # Add all flattened user fields
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        User.objects.filter(pk=instance.user_id).update(
            **user_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class StudentProfileSerializer(BaseProfileSerializer):

    username = serializers.CharField(source='user.username', required=False)
    email = serializers.CharField(source='user.email', required=False)
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
        source='user.profile_picture', required=False)  # Added profile_picture

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'username', 'email', 'name', 'role', 'contact', 'date_of_birth', 'address', 'nationality', 'government_id', 'profile_picture', 'level', 'program', 'intake', 'date_of_admission', 'tuition_fee', 'balance', 'remarks',
                  'medical_forms', 'admission_letter', 'payment_method', 'payment_status', 'payment_date', 'amount_due']  # Include flattened fields

    def create(self, validated_data):
        user_data = {}
        for field in ['username', 'email',  'name', 'role', 'contact', 'date_of_birth', 'address', 'nationality', 'government_id', 'profile_picture']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        # Create or update the user
        user, created = User.objects.update_or_create(  # Use update_or_create
            email=user_data.pop('email'), defaults=user_data
        )

        profile = StudentProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = {}
        for field in ['username', 'email',  'name', 'role', 'contact', 'date_of_birth', 'address', 'nationality', 'government_id', 'profile_picture']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        User.objects.filter(pk=instance.user_id).update(
            **user_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TeacherProfileSerializer(BaseProfileSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.CharField(source='user.email', required=False)
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
        model = TeacherProfile
        fields = ['id', 'user', 'username', 'email', 'name', 'role', 'contact', 'date_of_birth', 'address', 'nationality', 'government_id', 'subject_taught', 'profile_picture', 'department', 'date_of_employment',
                  'college_degree', 'teachers_in_the_same_program']

    def create(self, validated_data):
        user_data = {}
        for field in ['username', 'email',  'name', 'role', 'contact', 'date_of_birth', 'address', 'nationality', 'government_id', 'profile_picture']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        # Create or update the user
        user, created = User.objects.update_or_create(  # Use update_or_create
            email=user_data.pop('email'), defaults=user_data
        )

        profile = TeacherProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = {}
        for field in ['username', 'email',  'name', 'role', 'contact', 'date_of_birth', 'address', 'nationality', 'government_id', 'profile_picture']:  # Add all flattened user fields
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        User.objects.filter(pk=instance.user_id).update(
            **user_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class NonTeachingStaffProfileSerializer(BaseProfileSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.CharField(source='user.email', required=False)
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

    class Meta:
        model = NonTeachingStaffProfile
        fields = ['id', 'user', 'username', 'email', 'name', 'role', 'contact', 'date_of_birth', 'address',
                  'nationality', 'government_id', 'position', 'date_of_employment', 'department', 'college_degree']

    def create(self, validated_data):  # Correctly positioned outside Meta
        user_data = {}
        for field in ['username', 'email', 'name', 'role', 'contact', 'date_of_birth', 'address', 'nationality', 'government_id']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        user, created = User.objects.update_or_create(
            email=user_data.pop('email'), defaults=user_data
        )
        profile = NonTeachingStaffProfile.objects.create(
            user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = {}
        for field in ['username', 'email',  'name', 'role', 'contact', 'date_of_birth', 'address', 'nationality', 'government_id', 'profile_picture']:  # Add all flattened user fields
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        User.objects.filter(pk=instance.user_id).update(
            **user_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
