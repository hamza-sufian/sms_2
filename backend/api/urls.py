# urls.py in your app directory

from django.urls import path
from .views import (
    StudentProfileListCreateView,
    StudentProfileDetailView,
    TeacherProfileListCreateView,
    TeacherProfileDetailView,
    NonTeachingStaffProfileListCreateView,
    NonTeachingStaffProfileDetailView,
)

urlpatterns = [
    # Student profile URLs
    path('students/', StudentProfileListCreateView.as_view(),
         name='student-list-create'),
    path('students/<int:pk>/', StudentProfileDetailView.as_view(),
         name='student-detail'),

    # Teacher profile URLs
    path('teachers/', TeacherProfileListCreateView.as_view(),
         name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherProfileDetailView.as_view(),
         name='teacher-detail'),

    # Non-teaching staff profile URLs
    path('non-teaching-staff/', NonTeachingStaffProfileListCreateView.as_view(),
         name='non-teaching-staff-list-create'),
    path('non-teaching-staff/<int:pk>/',
         NonTeachingStaffProfileDetailView.as_view(), name='non-teaching-staff-detail'),
]
