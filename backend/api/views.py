from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import (
    StudentProfileSerializer,
    TeacherProfileSerializer,
    NonTeachingStaffProfileSerializer,
    UserSerializer
)
from .models import StudentProfile, TeacherProfile, NonTeachingStaffProfile, User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BaseProfileListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    @swagger_auto_schema(
        operation_description="Create a new profile",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Profile created successfully",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid data provided"
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BaseProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_description="Retrieve a profile",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Profile retrieved successfully",
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Profile not found"
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a profile",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Profile updated successfully",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid data provided"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Profile not found"
            ),
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a profile",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Profile deleted successfully"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Profile not found"
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class StudentProfileListCreateView(BaseProfileListCreateView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    filterset_fields = ['level', 'program', 'intake']
    search_fields = ['user__name', 'user__email', 'program']
    ordering_fields = ['user__name', 'level', 'program', 'intake']


class StudentProfileDetailView(BaseProfileDetailView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class TeacherProfileListCreateView(BaseProfileListCreateView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    filterset_fields = ['department', 'subject_taught']
    search_fields = ['user__name', 'user__email',
                     'department', 'subject_taught']
    ordering_fields = ['user__name', 'department', 'date_of_employment']


class TeacherProfileDetailView(BaseProfileDetailView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer


class NonTeachingStaffProfileListCreateView(BaseProfileListCreateView):
    queryset = NonTeachingStaffProfile.objects.all()
    serializer_class = NonTeachingStaffProfileSerializer
    filterset_fields = ['department', 'position']
    search_fields = ['user__name', 'user__email', 'department', 'position']
    ordering_fields = ['user__name', 'department', 'date_of_employment']


class NonTeachingStaffProfileDetailView(BaseProfileDetailView):
    queryset = NonTeachingStaffProfile.objects.all()
    serializer_class = NonTeachingStaffProfileSerializer
