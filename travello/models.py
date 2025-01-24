

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


class Availability(models.Model):
    guide = models.ForeignKey('Guide', on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.guide.first_name} {self.guide.last_name} available from {self.start_date} to {self.end_date}"

    def clean(self):
      
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after the start date.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)


class Destination(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)
    list_items = models.TextField(blank=True, null=True) # Add a field to store the bullent points

    def __str__(self):
        return self.name


from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class Guide(models.Model):
    CIVILITY_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
    ]

    civility = models.CharField(max_length=10, choices=CIVILITY_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100)
    city_or_region = models.CharField(max_length=100)
    mother_tongue = models.CharField(max_length=50)
    tour_languages = models.TextField(help_text="Comma-separated list of languages")
    presentation = models.TextField()
    photo = models.ImageField(upload_to="pics/")
    certified_guide = models.BooleanField(default=False)
    guide_card = models.FileField(upload_to="pics/", blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New price field
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Guide authentication fields
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Password field for hashing
    users = models.ManyToManyField('auth.User', blank=True, related_name='userss')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.country})"

    def save(self, *args, **kwargs):
        try:
            # Hash password if it’s not already hashed
            if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$')):
                self.password = make_password(self.password)
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error in save method: {e}")
            raise

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class Booking(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    preferred_date = models.DateField(null=True, blank=True) 
    party_size = models.PositiveIntegerField(default=1)  
    message = models.TextField()
    accept_terms = models.BooleanField(default=False)
    accept_marketing_emails = models.BooleanField(default=False)

    # ForeignKey to Guide
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='bookings')
    
    # ForeignKey to User
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='bookings')
    
    # Timestamp of the booking
    booking_date = models.DateTimeField(default=timezone.now)
    
    # Choices for booking status
    status_choices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"Booking by {self.first_name} {self.last_name} - {self.email}"

    def clean(self):
       
        if self.party_size < 1:
            raise ValidationError("Party size must be at least 1.")



class Message(models.Model):
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='received_messages')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)  # Add this field

    def __str__(self):
         return f"From {self.sender.username} to {self.recipient.first_name}"