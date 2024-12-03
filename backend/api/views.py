from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import StudentProfileSerializer, TeacherProfileSerializer, NonTeachingStaffProfileSerializer
from .models import StudentProfile, TeacherProfile, NonTeachingStaffProfile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BaseProfileListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Create a new profile",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BaseProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class StudentProfileListCreateView(BaseProfileListCreateView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    filterset_fields = ['level', 'program', 'intake']
    search_fields = ['user__name', 'user__email', 'program']
    ordering = ['-user__name', 'level', 'program', 'intake']
    ordering_fields = ['user__name', 'level', 'program', 'intake']

    @swagger_auto_schema(
        operation_description="Create a new student profile",
        request_body=StudentProfileSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description="Profile created successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data provided"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentProfileDetailView(BaseProfileDetailView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('profile_image', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('medical_forms', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('admission_letter', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
        ]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('profile_image', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('medical_forms', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('admission_letter', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
        ]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class TeacherProfileListCreateView(BaseProfileListCreateView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    filterset_fields = ['department', 'subject_taught']
    search_fields = ['user__name', 'user__email',
                     'department', 'subject_taught']
    ordering = ['-user__name', 'department', 'subject_taught']
    ordering_fields = ['user__name', 'department', 'date_of_employment']

    @swagger_auto_schema(
        operation_description="Create a new teacher profile",
        request_body=TeacherProfileSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description="Profile created successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data provided"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TeacherProfileDetailView(BaseProfileDetailView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('image', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
        ]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('image', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
        ]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class NonTeachingStaffProfileListCreateView(BaseProfileListCreateView):
    queryset = NonTeachingStaffProfile.objects.all()
    serializer_class = NonTeachingStaffProfileSerializer
    filterset_fields = ['department', 'position']
    search_fields = ['user__name', 'user__email', 'department', 'position']
    ordering = ['-user__name', 'department', 'position']
    ordering_fields = ['user__name', 'department', 'date_of_employment']

    @swagger_auto_schema(
        operation_description="Create a new non-teaching staff profile",
        request_body=NonTeachingStaffProfileSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(description="Profile created successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data provided"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class NonTeachingStaffProfileDetailView(BaseProfileDetailView):
    queryset = NonTeachingStaffProfile.objects.all()
    serializer_class = NonTeachingStaffProfileSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('image', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
        ]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('image', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=False),
        ]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
