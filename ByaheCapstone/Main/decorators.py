from django.shortcuts import redirect
from django.contrib import messages

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You do not have permission to access this page.    ")
            return redirect('signin')  # Redirect to login if not authenticated
        
        if not request.user.is_staff:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('logged_in')  # Redirect to home for non-admins
        
        return view_func(request, *args, **kwargs)
    return wrapper_func