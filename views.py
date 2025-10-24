# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailOTP
import random
import pytz
from datetime import datetime
from django.http import JsonResponse

User = get_user_model()

def home_view(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        timezone_sel = request.POST.get('timezone') or 'UTC'
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error':'Email already registered'})
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.timezone = timezone_sel
        user.save()

        # create OTP and send email
        code = "%06d" % random.randint(0, 999999)
        otp = EmailOTP.objects.create(user=user, code=code)
        send_mail(
            'Privacy Locker - Registration OTP',
            f'Your OTP: {code}',
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        # Show a page instructing OTP verification (we can reuse register.html with flag)
        return render(request, 'register.html', {'otp_sent': True, 'email': email})
    else:
        return render(request, 'register.html')

def verify_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('otp')
        try:
            user = User.objects.get(username=email)
            otp = EmailOTP.objects.filter(user=user, code=code).order_by('-created_at').first()
            if otp and otp.is_valid():
                # OTP valid — can mark email verified (optional)
                return redirect('login')
            else:
                return render(request, 'register.html', {'otp_error': 'Invalid or expired OTP', 'email': email})
        except User.DoesNotExist:
            return redirect('register')
    return redirect('register')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return render(request, 'index.html', {'login_error':'Invalid credentials'})

        user_auth = authenticate(request, username=email, password=password)
        if user_auth:
            user.reset_failed()
            login(request, user_auth)
            return redirect('secure_data')
        else:
            user.failed_attempts += 1
            user.save()
            if user.failed_attempts >= 3:
                # Send alert email and reset failed_attempts (or lock account)
                send_mail(
                    'Privacy Locker - Alert: Multiple Failed Login Attempts',
                    'There were 3 failed login attempts to your account. If this wasn\'t you, reset your password immediately.',
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                # optional: lock account or reset counter
                user.failed_attempts = 0
                user.save()
                return render(request, 'index.html', {'login_error': '3 failed attempts — alert email sent.'})
            return render(request, 'index.html', {'login_error': 'Invalid credentials.'})
    return render(request, 'index.html')
