from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Car(models.Model):
    CATEGORY_CHOICES = [
        ('sedan', 'Sedan'), ('suv', 'SUV'), ('luxury', 'Luxury'),
        ('pickup', 'Pickup'), ('hatchback', 'Hatchback'),
    ]
    TRANSMISSION_CHOICES = [('manual', 'Manual'), ('automatic', 'Automatic')]
    car_id = models.IntegerField(default=0)
    car_name = models.CharField(max_length=50)
    car_desc = models.CharField(max_length=500, blank=True)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to="car/images", blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='sedan')
    is_available = models.BooleanField(default=True)
    seating_capacity = models.IntegerField(default=5)
    fuel_type = models.CharField(max_length=20, default="Petrol")
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, default='manual')
    mileage_kmpl = models.DecimalField(max_digits=4, decimal_places=1, default=18.0)
    year = models.IntegerField(default=2024)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.car_name


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'), ('confirmed', 'Confirmed'),
        ('completed', 'Completed'), ('cancelled', 'Cancelled'),
    ]
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=90)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=50, blank=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    car_name = models.CharField(max_length=50)
    days_for_rent = models.PositiveIntegerField()
    price_per_day = models.IntegerField()
    total_price = models.IntegerField()
    pickup_date = models.DateField()
    loc_from = models.CharField(max_length=100)
    loc_to = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.car_name} - {self.name}"


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username
