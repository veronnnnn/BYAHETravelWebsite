from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),

    path('signup/', views.SignUpView, name='signup'),
    path('login/', views.SignInView, name='signin'),
    path('logged_in/', views.LoggedInView, name='logged_in'),
    path('logout/', views.LogOutView, name='logout'),

    path('forgot_password/', views.ForgotPassword, name='forgot_password'),
    path('password-reset-sent/<str:reset_id>/', views.ForgotPass2, name='forgot_pass2'),
    path('change_password/<str:reset_id>/', views.ChangePassword, name='change_password'),  # Corrected
]
