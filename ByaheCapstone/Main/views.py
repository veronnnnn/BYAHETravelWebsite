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
from .models import Profile, Reservation
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import ReservationForm
from django.http import JsonResponse
from .decorators import admin_only


#HOMEPAGE
def Home(request):
    return render(request, 'index.html')
#ADMIN DASHBOARD

def admin_dashboard(request):
    
    # Fetch data from the database
    users = User.objects.all()
    reservations = Reservation.objects.all()

    return render(request, 'admin/admin_index.html', {
        'users': users,
        'reservations': reservations,
    })

#ADMIN user profiles

def admin_users(request):
    # Fetch data from the database
    
    users = User.objects.all()

    return render(request, 'admin/users.html', {
        'users': users,
    })

def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('admin_users')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use another one.")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, "User added successfully!")

        return redirect('admin_users')

    return redirect('admin_users') 


def add_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('admin_users')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('admin_users')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect('admin_users')

        # Create the admin user
        admin_user = User.objects.create_user(username=username, email=email, password=password)
        admin_user.is_staff = True  # Mark the user as an admin
        admin_user.save()

        messages.success(request, "Admin created successfully.")
        return redirect('admin_users')

    return redirect('admin_users')

def add_driver(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contact_number = request.POST['contact_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('admin_dashboard')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('admin_dashboard')

        # Create the driver user
        driver = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        driver.is_driver = True  # Custom field to mark as a driver
        driver.contact_number = contact_number
        driver.save()

        messages.success(request, "Driver added successfully!")
        return redirect('admin_dashboard')

#ADMIN delete user

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('admin_users')  # Replace with the name of the URL pattern for the user profiles page
    return render(request, 'delete_user_confirmation.html', {'user': user})

#Check if Admin or not
def some_view(request):
    # Example: Admin check
    if not request.user.is_staff:  # Or your custom check
        messages.error(request, "You are not authorized to access the admin dashboard.")
        return render(request, 'logged_in.html')  # Renders the template directly to process messages
    
    # Logic for authorized users
    return render(request, 'admin_index.html')


#DRIVERS

def driver_dashboard(request):
    
    # Fetch data from the database
    users = User.objects.all()
    reservations = Reservation.objects.all()

    return render(request, 'admin/drivers.html', {
        'users': users,
        'reservations': reservations,
    })


def admin_tracking(request):
    
    # Fetch data from the database
    users = User.objects.all()
    reservations = Reservation.objects.all()

    return render(request, 'admin/tracking.html', {
        'users': users,
        'reservations': reservations,
    })


def admin_vehicles(request):
    
    # Fetch data from the database
    users = User.objects.all()
    reservations = Reservation.objects.all()

    return render(request, 'admin/vehicles.html', {
        'users': users,
        'reservations': reservations,
    })

def admin_payment(request):
    
    # Fetch data from the database
    users = User.objects.all()
    reservations = Reservation.objects.all()

    return render(request, 'admin/payment.html', {
        'users': users,
        'reservations': reservations,
    })

def admin_reviews(request):
    
    # Fetch data from the database
    users = User.objects.all()
    reservations = Reservation.objects.all()

    return render(request, 'admin/reviews.html', {
        'users': users,
        'reservations': reservations,
    })


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

            # Check if the logged-in user is a superuser
            if user.is_staff:
                return redirect('admin_dashboard')  # Replace 'admin_index' with the name of the admin dashboard URL pattern
            
            return redirect('logged_in')  # Redirect regular users to the logged-in page
            

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

def reservation_form_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, request.FILES)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user

            # Define distance map for routes
            distance_map = {
                ('lucban_terminal', 'lucena_grand_terminal'): 23.2,
                ('lucban_terminal', 'tayabas_city_public_market'): 12.9,
                ('tayabas_city_public_market', 'lucena_grand_terminal'): 9.2,
            }

            # Extract pickup and dropoff locations from the form
            pickup_location_key = reservation.pickup_location.split('_pick')[0]
            dropoff_location_key = reservation.dropoff_location.split('_drop')[0]

            # Get the distance for the selected route
            distance = distance_map.get((pickup_location_key, dropoff_location_key), 0)

            # Define fare computation constants
            fare_per_km = 17 / 4  # 17 pesos per 4 kilometers
            base_fare = distance * fare_per_km

            # Map vehicle to seat count
            seat_map = {
                'Toyota Corolla': 6,
                'Modernized PUV V1': 15,
                'Modernized PUV V2': 15,
            }
            seat_count = seat_map.get(reservation.vehicle, 0)

            # Calculate total fare
            total_fare = base_fare * seat_count
            if reservation.roundtrip:
                total_fare *= 2  # Double the fare for roundtrip

            # Assign the calculated total fare
            reservation.total_fare = round(total_fare, 2)

            # Save the reservation
            reservation.save()
            print("Form valid")

            # Redirect to a success page
            return redirect('reservation_success', reservation_id=reservation.id)
        else:
            print("Reservation Form is not valid!")
            print(form.errors)  # Print the form errors to see what's wrong
            return render(request, 'reservation/reservation-form.html', {'form': form})
    else:
        form = ReservationForm()
        return render(request, 'reservation/reservation-form.html', {'form': form})

def CalculateFareView(request):
    if request.method == "POST":
        pickup_location = request.POST.get('pickup_location')
        dropoff_location = request.POST.get('dropoff_location')
        vehicle = request.POST.get('vehicle')

        # Example fare calculation logic
        fare = 0
        if pickup_location and dropoff_location and vehicle:
            if pickup_location == "A" and dropoff_location == "B":
                fare = 500
            if vehicle == "Toyota Corolla":
                fare += 100

        return JsonResponse({'fare': fare})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def ReservationSuccessView(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    return render(request, 'reservation/reservation-success.html', {'reservation': reservation})

