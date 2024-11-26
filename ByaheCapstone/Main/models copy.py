from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name or ''}"

    def __str__(self):
        return self.user.username

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"
    

#MODELS FOR RESERVATION FORM
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who made the reservation
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    
    # Date and Time Fields
    pickup_date = models.DateField(null=True, blank=True)
    dropoff_date = models.DateField(null=True, blank=True)
    pickup_time = models.TimeField(null=True, blank=True)
    dropoff_time = models.TimeField(null=True, blank=True)

    PICKUP_LOCATION_CHOICES = [
        ('lucena_grand_terminal_pick', 'Lucena Grand Terminal'),
        ('groto_lucban_quezon_pick', 'Groto Lucban Quezon'),
        ('tayabas_city_quezon_pick', 'Tayabas City Quezon'),
    ]
    
    DROPOFF_LOCATION_CHOICES = [
        ('lucena_grand_terminal_drop', 'Lucena Grand Terminal'),
        ('groto_lucban_quezon_drop', 'Groto Lucban Quezon'),
        ('tayabas_city_quezon_drop', 'Tayabas City Quezon'),
    ]

    # Location Fields
    pickup_location = models.CharField(max_length=255, choices= PICKUP_LOCATION_CHOICES)
    dropoff_location = models.CharField(max_length=255, choices= DROPOFF_LOCATION_CHOICES)

    #     # Location Fields
    # pickup_location = models.CharField(max_length=255)
    # dropoff_location = models.CharField(max_length=255)
    
    # Vehicle and Payment
    vehicle = models.CharField(max_length=100, choices=[
        ('Toyota Corolla', 'Class A - Toyota Corolla - 6 Seats'),
        ('Modernized PUV V1', 'Class B - Modernized PUV V1 - 15 Seats'),
        ('Modernized PUV V2', 'Class B - Modernized PUV V2 - 15 Seats'),
    ])
    payment_method = models.CharField(max_length=20, choices=[
        ('gcash', 'GCash'),
        ('cash', 'On-hand Payment (CASH)')
    ])
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    roundtrip = models.BooleanField(default=False)

    # GCash Receipt Upload
    gcash_receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.full_name} ({self.pickup_date})"
    
