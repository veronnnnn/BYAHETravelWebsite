from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'full_name', 'contact_number', 'pickup_date', 'dropoff_date',
            'pickup_time', 'dropoff_time', 'pickup_location', 'dropoff_location',
            'vehicle', 'payment_method', 'total_fare', 'roundtrip', 'gcash_receipt'
        ]
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'dropoff_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
            'dropoff_time': forms.TimeInput(attrs={'type': 'time'}),
            'gcash_receipt': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }