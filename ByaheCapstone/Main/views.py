from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from .models import Profile

def Home(request):
    return render(request, 'index.html')

def SignUpView(request):

    if request.method == "POST":

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, 'Username already exists')

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email already exists')

        if len(password) < 8:
            user_data_has_error = True
            messages.error(request, "Password should be at least 8 characters long")

        if password != confirm_password:
            user_data_has_error = True
            messages.error(request, "Passwords do not match")

        if user_data_has_error :
            return redirect('signup')
        else: 
            new_user = User.objects.create_user(

                username = username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
            )

            # Create Profile with additional fields
            Profile.objects.create(
                user=new_user,
                contact_number=contact_number,
                address=address,
            )

            messages.success(request, 'Account created successfully. Please log in now')
            return redirect('signin')

    return render(request, 'sign-up.html')

    

def SignInView(request):
    return render(request, 'sign-in.html')


def ForgotPasswordView(request):
    return render(request, 'forgot-password.html')