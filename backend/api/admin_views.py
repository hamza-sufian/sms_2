from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from .models import OTP
from .tasks import send_otp_email
from datetime import timedelta
from django.utils.timezone import now
import random

class AdminOTPLoginView(LoginView):
    template_name = 'admin/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff:
            otp_code = f"{random.randint(100000, 999999)}"
            expiration_time = now() + timedelta(minutes=10)
            OTP.objects.update_or_create(user=user, defaults={"code": otp_code, "expiration_time": expiration_time})
            send_otp_email.delay(user.id, otp_code)
            self.request.session['admin_user_id'] = user.id
            return redirect('admin_otp_verify')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class AdminOTPVerifyView(View):
    def get(self, request):
        return render(request, 'admin/otp_verify.html')

    def post(self, request):
        otp_code = request.POST.get('otp')
        user_id = request.session.get('admin_user_id')
        if not user_id:
            return redirect('admin:login')

        try:
            user = User.objects.get(id=user_id)
            otp = OTP.objects.get(user=user)
        except (User.DoesNotExist, OTP.DoesNotExist):
            return render(request, 'admin/otp_verify.html', {'error': 'Invalid OTP.'})

        if otp.code != otp_code:
            return render(request, 'admin/otp_verify.html', {'error': 'Invalid OTP.'})

        if now() > otp.expiration_time:
            return render(request, 'admin/otp_verify.html', {'error': 'OTP has expired.'})

        otp.delete()
        del request.session['admin_user_id']
        return redirect('admin:index')