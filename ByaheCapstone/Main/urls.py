from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),

    path('signup/', views.SignUpView, name='signup'),
    path('login/', views.SignInView, name='signin'),

    path('forgot_password/', views.ForgotPasswordView, name='forgot_password'),

]
