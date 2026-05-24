from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    CATEGORY_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('luxury', 'Luxury'),
        ('pickup', 'Pickup'),
        ('hatchback', 'Hatchback'),
    ]
    car_id = models.IntegerField(default=0)
    car_name = models.CharField(max_length=30, default="")
    car_desc = models.CharField(max_length=300, default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="car/images", default="")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='sedan')
    is_available = models.BooleanField(default=True)
    seating_capacity = models.IntegerField(default=5)
    fuel_type = models.CharField(max_length=20, default="Petrol")

    def __str__(self):
        return self.car_name


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=90, default="")
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    car_name = models.CharField(max_length=50, default="")
    days_for_rent = models.IntegerField(default=0)
    price_per_day = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    date = models.CharField(max_length=50, default="")
    loc_from = models.CharField(max_length=50, default="")
    loc_to = models.CharField(max_length=50, default="")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_name} - {self.name}"


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, default="")
    email = models.CharField(max_length=150, default="")
    phone_number = models.CharField(max_length=15, default="")
    message = models.TextField(max_length=500, default="")

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.user.username
