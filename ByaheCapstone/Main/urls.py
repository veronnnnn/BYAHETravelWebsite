from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),

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

    #reservation success
    path('reservation/success/', views.ReservationSuccessView, name='reservation_success'),
]
