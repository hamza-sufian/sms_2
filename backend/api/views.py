from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StudentProfileListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    @swagger_auto_schema(
        operation_description="Create a new student profile",
        request_body=StudentProfileSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Student profile created successfully",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid data provided"
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    pagination_class = StandardResultsSetPagination

    @ swagger_auto_schema(
        operation_description="Get a list of all student profiles",
        manual_parameters=[
            openapi.Parameter('level', openapi.IN_QUERY,
                              description="Filter by student level", type=openapi.TYPE_INTEGER),
            openapi.Parameter('program', openapi.IN_QUERY,
                              description="Filter by program", type=openapi.TYPE_STRING),
            openapi.Parameter('intake', openapi.IN_QUERY,
                              description="Filter by intake", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY,
                              description="Search term for student profiles", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY,
                              description="Order by field (e.g., 'name', '-level')", type=openapi.TYPE_STRING),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='A list of student profiles',
                examples={
                    'application/json': [
                        {
                            "id": "23-00001",
                            "user": {
                                "id": 1,
                                "username": "john.doe",
                                "email": "john.doe@example.com",
                                "name": "John Doe",
                                "contact": "1234567890",
                                "date_of_birth": "2000-01-01",
                                "address": "123 Main St",
                                "nationality": "American",
                                "government_id": "A12345678",
                                "email_verified": True,
                            },
                            "level": 100,
                            "program": "OFAD",
                            "intake": "2023",
                            "tuition_fee": 10000.00,
                            "balance": 5000.00,
                            "remarks": "Excellent",
                            "profile_image": "/path/to/image.jpg",
                            "amount_due": 5000.00,
                            "medical_forms": "/path/to/form.pdf",
                            "admission_letter": "/path/to/admission.pdf",
                            "payment_method": "Credit Card",
                            "payment_status": "Paid",
                            "payment_date": "2023-06-15",
                        }
                    ]
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='Invalid query parameters',
                examples={
                    'application/json': {
                        "detail": "Invalid level provided. Level must be an integer."
                    }
                }
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a student profile",
        request_body=StudentProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Student profile updated successfully",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid data provided"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Student profile not found"
            ),
        }
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a student profile",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Student profile deleted successfully"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Student profile not found"
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# View for TeacherProfile CRUD operations


class TeacherProfileListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    @swagger_auto_schema(
        operation_description="Create a new teacher profile",
        request_body=TeacherProfileSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Teacher profile created successfully",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid data provided"
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_description="Retrieve a teacher profile",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Teacher profile retrieved successfully",
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Teacher profile not found"
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a teacher profile",
        request_body=TeacherProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Teacher profile updated successfully",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid data provided"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Teacher profile not found"
            ),
        }
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a teacher profile",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Teacher profile deleted successfully"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Teacher profile not found"
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# View for NonTeachingStaffProfile CRUD operations


class NonTeachingStaffProfileListCreateView(generics.ListCreateAPIView):
    # Ensure the correct model for non-teaching staff
    permission_classes = [IsAuthenticated]
    queryset = NonTeachingStaffProfile.objects.all()
    serializer_class = NonTeachingStaffProfileSerializer

    @swagger_auto_schema(
        operation_description="Create a new non-teaching staff profile",
        request_body=NonTeachingStaffProfileSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Non-teaching staff profile created successfully",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid data provided"
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NonTeachingStaffProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Ensure the correct model for non-teaching staff
    permission_classes = [IsAuthenticated]
    queryset = NonTeachingStaffProfile.objects.all()
    serializer_class = NonTeachingStaffProfileSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_description="Retrieve a non-teaching staff profile",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Non-teaching staff profile retrieved successfully",
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Non-teaching staff profile not found"
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a non-teaching staff profile",
        request_body=NonTeachingStaffProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Non-teaching staff profile updated successfully",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid data provided"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Non-teaching staff profile not found"
            ),
        }
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a non-teaching staff profile",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Non-teaching staff profile deleted successfully"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Non-teaching staff profile not found"
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
