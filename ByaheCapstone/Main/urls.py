from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),  

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_users/', views.admin_users, name='admin_users'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'), #DELETE USER
    path('add-user/', views.add_user, name='add_user'), #ADD USER
    path('add-admin/', views.add_admin, name='add_admin'), #ADD ADMIN
    path('add-driver/', views.add_driver, name='add_driver'), #ADD DRIVER

    path('driver_dashboard/', views.driver_dashboard, name='driver_dashboard'),

    path('admin_vehicles/', views.admin_vehicles, name='admin_vehicles'),
    path('admin_tracking/', views.admin_tracking, name='admin_tracking'),
    path('admin_payment/', views.admin_payment, name='admin_payment'),
    path('admin_reviews/', views.admin_payment, name='admin_reviews'),


    path('signup/', views.SignUpView, name='signup'),
    path('login/', views.SignInView, name='signin'),
    path('logged_in/', views.LoggedInView, name='logged_in'),
    path('logout/', views.LogOutView, name='logout'),

    path('taxi1/', views.TaxiView1, name='taxi1'),
    path('taxi2/', views.TaxiView2, name='taxi2'),
    path('taxi3/', views.TaxiView3, name='taxi3'),
    path('minibus1/', views.MiniBusView1, name='minibus1'),
    path('minibus2/', views.MiniBusView2, name='minibus2'),
    path('minibus3/', views.MiniBusView3, name='minibus3'),
        

    path('forgot_password/', views.ForgotPassword, name='forgot_password'),
    path('password-reset-sent/<str:reset_id>/', views.ForgotPass2, name='forgot_pass2'),
    path('change_password/<str:reset_id>/', views.ChangePassword, name='change_password'),  # Corrected

    # Reservation form page
    path('reservation/', views.reservation_form_view, name='reservation_form_view'),
    #reservation calculate fare
    path('calculate-fare/', views.CalculateFareView, name='calculate_fare'),


    #reservation success
    path('reservation/success/<int:reservation_id>/', views.ReservationSuccessView, name='reservation_success'),
]
