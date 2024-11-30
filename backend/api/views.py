from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.mail import send_mail
from django.conf import settings
from .models import User, OTP
from .serializers import UserSerializer
from datetime import timedelta
import random
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

class AdminCreateUserView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Create a new user and send credentials to their email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the user'),
                'role': openapi.Schema(type=openapi.TYPE_STRING, description='Role of the user', enum=['STUDENT', 'TEACHING_STAFF', 'NON_TEACHING_STAFF']),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name of the user'),
                'contact': openapi.Schema(type=openapi.TYPE_STRING, description='Contact number of the user'),
                'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date of birth of the user'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s address'),
                'nationality': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s nationality'),
                'government_id': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s government-issued ID'),
                'profile_picture': openapi.Schema(type=openapi.TYPE_FILE, description='Profile picture of the user'),
            },
            required=['username', 'email', 'password', 'role']
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="User created successfully.",
                examples={
                    'application/json': {
                        "message": "User created successfully, credentials sent to email."
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input data.",
                examples={
                    'application/json': {
                        "detail": "Some required fields are missing or invalid."
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            password = request.data['password']

            # Send credentials to user via email
            subject = "Your account credentials"
            message = f"""
            Hello {user.username},

            Your account has been created successfully.
            Username: {user.username}
            Password: {password}

            Please login to access your account.
            """
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            except Exception as e:
                return Response({"error": "User created, but email could not be sent.", "details": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "User created successfully, credentials sent to email."},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve user details or list of all users.",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="User details",
                examples={
                    'application/json': {
                        "id": "1",
                        "username": "john_doe",
                        "email": "john.doe@example.com",
                        "role": "STUDENT",
                        "name": "John Doe",
                        "contact": "123456789",
                        "date_of_birth": "2000-01-01",
                        "address": "123 Street Name",
                        "nationality": "Ghanaian",
                        "government_id": "GHA-123456",
                        "profile_picture": "http://example.com/image.jpg"
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid query parameters",
                examples={
                    'application/json': {
                        "detail": "Invalid request format"
                    }
                }
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update user details.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s email address'),
                'role': openapi.Schema(type=openapi.TYPE_STRING, description='Role of the user'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name of the user'),
                'contact': openapi.Schema(type=openapi.TYPE_STRING, description='Contact number of the user'),
                'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date of birth of the user'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s address'),
                'nationality': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s nationality'),
                'government_id': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s government-issued ID'),
                'profile_picture': openapi.Schema(type=openapi.TYPE_FILE, description='Profile picture of the user'),
            },
            required=['email']
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="User updated successfully.",
                examples={
                    'application/json': {
                        "message": "User updated successfully.",
                        "data": {
                            "id": "1",
                            "username": "john_doe",
                            "email": "john.doe@example.com",
                            "role": "STUDENT"
                        }
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input data.",
                examples={
                    'application/json': {
                        "detail": "Some fields are invalid."
                    }
                }
            )
        }
    )
    def put(self, request, *args, **kwargs):
        user_id = self.request.data.get('id')
        if not user_id:
            return Response({"error": "User ID is required to update a user."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID to delete")
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="User deleted successfully.",
                examples={
                    'application/json': {
                        "message": "User deleted successfully."
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input data.",
                examples={
                    'application/json': {
                        "detail": "User ID is required."
                    }
                }
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        user_id = self.request.data.get('id')
        if not user_id:
            return Response({"error": "User ID is required to delete a user."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)


class OTPLoginView(APIView):
    @swagger_auto_schema(
        operation_description="Generate OTP and send to user's email for login",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="OTP sent to email",
                examples={
                    'application/json': {
                        "message": "OTP sent to your email."
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Email is required",
                examples={
                    'application/json': {
                        "error": "Email is required."
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP
        otp_code = f"{random.randint(100000, 999999)}"
        expiration_time = now() + timedelta(minutes=10)

        # Store OTP in the database
        OTP.objects.update_or_create(user=user, defaults={"code": otp_code, "expiration_time": expiration_time})

        # Send OTP to user's email
        subject = "Your OTP Code"
        message = f"""
        Hello {user.username},

        Your OTP code for logging in is: {otp_code}
        It will expire in 10 minutes.
        """
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        except Exception as e:
            return Response({"error": "OTP could not be sent.", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
    @swagger_auto_schema(
        operation_description="Verify OTP for login",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="OTP verified successfully",
                examples={
                    'application/json': {
                        "message": "OTP verified successfully."
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid OTP or OTP expired",
                examples={
                    'application/json': {
                        "error": "Invalid OTP or OTP has expired."
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp_code = request.data.get('otp')

        if not email or not otp_code:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.get(user=user)
        except (User.DoesNotExist, OTP.DoesNotExist):
            return Response({"error": "Invalid email or OTP."}, status=status.HTTP_404_NOT_FOUND)

        # Check if OTP is valid
        if otp.code != otp_code:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        if now() > otp.expiration_time:
            return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        # OTP verified successfully
        return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
