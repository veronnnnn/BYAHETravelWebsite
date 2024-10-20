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
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'dropoff_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
            'dropoff_time': forms.TimeInput(attrs={'type': 'time'}),
            'pickup_location': forms.Select(choices=Reservation.PICKUP_LOCATION_CHOICES, attrs={'class': 'form-control'}),
            'dropoff_location': forms.Select(choices=Reservation.DROPOFF_LOCATION_CHOICES, attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'total_fare': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'roundtrip': forms.CheckboxInput(),
            'gcash_receipt': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }