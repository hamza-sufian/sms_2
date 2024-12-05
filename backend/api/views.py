from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import (
    StudentProfileSerializer,
    TeacherProfileSerializer,
    NonTeachingStaffProfileSerializer
)
from .models import (
    StudentProfile,
    TeacherProfile,
    NonTeachingStaffProfile
)
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

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BaseProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


### STUDENT PROFILE VIEWS ###
class StudentProfileListCreateView(BaseProfileListCreateView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    filterset_fields = ['level', 'program',
                        'intake', 'username', 'email']
    search_fields = ['username', 'email',
                     'program', 'level']
    ordering = ['-username', 'level', 'program', 'intake']
    ordering_fields = ['username',
                       'email', 'level', 'program', 'intake']

    @swagger_auto_schema(
        operation_description="Create a new student profile",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, description="Username",
                              type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('email', openapi.IN_FORM, description="Email address",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, required=True),
            openapi.Parameter('name', openapi.IN_FORM, description="Name",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('role', openapi.IN_FORM, description="Role",
                              type=openapi.TYPE_STRING, enum=["STUDENT"], required=False),
            openapi.Parameter('contact', openapi.IN_FORM, description="Contact number",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('date_of_birth', openapi.IN_FORM, description="Date of Birth",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
            openapi.Parameter('address', openapi.IN_FORM, description="Address",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('nationality', openapi.IN_FORM,
                              description="Nationality", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('government_id', openapi.IN_FORM,
                              description="Government ID", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('profile_picture', openapi.IN_FORM,
                              description="Profile picture", type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('level', openapi.IN_FORM, description="Student level",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('program', openapi.IN_FORM, description="Program",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('intake', openapi.IN_FORM, description="Intake",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('date_of_admission', openapi.IN_FORM, description="Date of admission",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
            openapi.Parameter('tuition_fee', openapi.IN_FORM,
                              description="Tuition fee", type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter('balance', openapi.IN_FORM, description="Balance",
                              type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter('remarks', openapi.IN_FORM, description="Remarks",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('medical_forms', openapi.IN_FORM,
                              description="Medical forms", type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('admission_letter', openapi.IN_FORM,
                              description="Admission letter", type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('payment_method', openapi.IN_FORM,
                              description="Payment method", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('payment_status', openapi.IN_FORM,
                              description="Payment status", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('payment_date', openapi.IN_FORM, description="Payment date",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
            openapi.Parameter('amount_due', openapi.IN_FORM,
                              description="Amount due", type=openapi.TYPE_NUMBER, required=False),
        ],
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
        operation_description="Update a student profile",
        request_body=StudentProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description="Profile updated successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data provided"),
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a student profile",
        request_body=StudentProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description="Profile updated successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data provided"),
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class TeacherProfileListCreateView(BaseProfileListCreateView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    filterset_fields = ['department', 'subject_taught',
                        'username', 'email']
    search_fields = ['username', 'email',
                     'department', 'subject_taught']
    ordering = ['-username', 'department', 'subject_taught']
    ordering_fields = ['username', 'email',
                       'department', 'subject_taught', 'date_of_employment']

    @swagger_auto_schema(
        operation_description="Create a new teacher profile",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, description="Username",
                              type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('email', openapi.IN_FORM, description="Email address",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, required=True),
            openapi.Parameter('name', openapi.IN_FORM, description="Name",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('role', openapi.IN_FORM, description="Role",
                              type=openapi.TYPE_STRING, enum=["TEACHING_STAFF"], required=False),
            openapi.Parameter('contact', openapi.IN_FORM, description="Contact number",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('date_of_birth', openapi.IN_FORM, description="Date of Birth",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
            openapi.Parameter('address', openapi.IN_FORM, description="Address",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('nationality', openapi.IN_FORM,
                              description="Nationality", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('government_id', openapi.IN_FORM,
                              description="Government ID", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('profile_picture', openapi.IN_FORM,
                              description="Profile picture", type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('department', openapi.IN_FORM,
                              description="Department", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('subject_taught', openapi.IN_FORM,
                              description="Subject taught", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('date_of_employment', openapi.IN_FORM,
                              description="Date of employment", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
            openapi.Parameter('college_degree', openapi.IN_FORM,
                              description="College degree", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('teachers_in_the_same_program', openapi.IN_FORM,
                              description="Teachers in the same program", type=openapi.TYPE_STRING, required=False),

        ],
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
        operation_description="Update a teacher profile",
        request_body=TeacherProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description="Profile updated successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data provided"),
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a teacher profile",
        request_body=TeacherProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description="Profile updated successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data provided"),
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class NonTeachingStaffProfileListCreateView(BaseProfileListCreateView):
    queryset = NonTeachingStaffProfile.objects.all()
    serializer_class = NonTeachingStaffProfileSerializer
    filterset_fields = ['department', 'position',
                        'username', 'email']
    search_fields = ['username', 'email',
                     'department', 'position']
    ordering = ['-username', 'department', 'position']
    ordering_fields = ['username', 'email',
                       'department', 'position', 'date_of_employment']

    @swagger_auto_schema(
        operation_description="Create a new non-teaching staff profile",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, description="Username",
                              type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('email', openapi.IN_FORM, description="Email address",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, required=True),
            openapi.Parameter('name', openapi.IN_FORM, description="Name",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('role', openapi.IN_FORM, description="Role",
                              type=openapi.TYPE_STRING, enum=["NON_TEACHING_STAFF"], required=False),
            openapi.Parameter('contact', openapi.IN_FORM, description="Contact number",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('date_of_birth', openapi.IN_FORM, description="Date of Birth",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
            openapi.Parameter('address', openapi.IN_FORM, description="Address",
                              type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('nationality', openapi.IN_FORM,
                              description="Nationality", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('government_id', openapi.IN_FORM,
                              description="Government ID", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('profile_picture', openapi.IN_FORM,
                              description="Profile picture", type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('department', openapi.IN_FORM,
                              description="Department", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('position', openapi.IN_FORM,
                              description="Position", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('date_of_employment', openapi.IN_FORM,
                              description="Date of employment", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
            openapi.Parameter('college_degree', openapi.IN_FORM,
                              description="College degree", type=openapi.TYPE_STRING, required=False),
        ],
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
        operation_description="Update a non-teaching staff profile",
        request_body=NonTeachingStaffProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description="Profile updated successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data provided"),
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a non-teaching staff profile",
        request_body=NonTeachingStaffProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description="Profile updated successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data provided"),
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
