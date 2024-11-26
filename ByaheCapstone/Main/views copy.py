from django.shortcuts import render, redirect, get_object_or_404
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
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import ReservationForm


def Home(request):
    return render(request, 'index.html')
@login_required
def LoggedInView(request):
    return render(request, 'index-logged.html')

def LogOutView(request):
    logout(request)
    return redirect('signin')

def TaxiView1(request):
    return render(request, 'vehicles/taxi1.html')

def TaxiView2(request):
    return render(request, 'vehicles/taxi2.html')

def TaxiView3(request):
    return render(request, 'vehicles/taxi3.html')

def MiniBusView1(request):
    return render(request, 'vehicles/minibus1.html')

def MiniBusView2(request):
    return render(request, 'vehicles/minibus2.html')

def MiniBusView3(request):
    return render(request, 'vehicles/minibus3.html')

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

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('logged_in')
        
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('signin')
        
    return render(request, 'sign-in.html')
    


def ForgotPassword(request):

    if request.method == "POST":
        email = request.POST.get("email")

    if request.method == 'POST':
        email = request.POST.get('email')

        # verify if email exists
        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('change_password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url =  f'{request.scheme}://{request.get_host()}{password_reset_url}'
            
            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
            'Reset your password', # email subject
            email_body,
            settings.EMAIL_HOST_USER, # email sender
            [email] # email  receiver 
        )
            
            email_message.fail_silently = True
            email_message.send()

            return render(request, 'forgot-pass2.html', {'reset_id':  new_password_reset.reset_id})

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot_password')

    return render(request, 'forgot-password.html')

@login_required
def ForgotPass2(request, reset_id): #password reset sent view

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'forgot-pass2.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'forgot-password2.html')

def ChangePassword(request, reset_id):
    
    try:
        # Retrieve the PasswordReset object using the UUID
        password_reset_entry = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 8:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 8 characters long')

            # Check if the link has expired
            expiration_time = password_reset_entry.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')
                password_reset_entry.delete()

            if not passwords_have_error:
                user = password_reset_entry.user
                user.set_password(password)
                user.save()

                # Delete reset entry after use
                password_reset_entry.delete()

                # Redirect to login
                messages.success(request, 'Password reset. Proceed to login')
                return redirect('signin')
        
        # If it's a GET request or there's an error, render the change password page
        return render(request, 'change-pass.html')

    except PasswordReset.DoesNotExist:
        # Redirect to forgot password page if the reset id does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot_password')

        return render(request, 'change-pass.html')

#reservation form view
@login_required
def reservation_form_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, request.FILES)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            print("form valid")
            # Save the form data to the database
            # form.save()
            # Redirect to a success page
            return redirect('reservation_success', reservation_id=reservation.id)
        else:
            print("Reservation Form is not valid!")
            print(form.errors)  # Print the form errors to see what's wrong
            return render(request, 'reservation/reservation-form.html', {'form': form})
    else:   
        form = ReservationForm()
        return render(request, 'reservation/reservation-form.html', {'form': form})

@login_required
def ReservationSuccessView(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    return render(request, 'reservation/reservation-success.html', {'reservation': reservation})

