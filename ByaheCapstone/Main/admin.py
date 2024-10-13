from django.contrib import admin
from .models import PasswordReset
from .models import Reservation

admin.site.register(PasswordReset)
# Register your models here.


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'contact_number', 'pickup_date', 'dropoff_date', 'vehicle', 'created_at')