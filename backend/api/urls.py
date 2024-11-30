from django.urls import path
from .views import AdminCreateUserView, OTPLoginView, OTPVerifyView

urlpatterns = [
    # URL for creating, retrieving, updating, and deleting users
    path('admin/users/', AdminCreateUserView.as_view(), name='admin-create-user'),
    
    # URL for OTP login
    path('otp-login/', OTPLoginView.as_view(), name='otp-login'),
    
    # URL for OTP verification
    path('verify-otp/', OTPVerifyView.as_view(), name='otp-verify'),
]
