from django.contrib import admin
from .models import Car, Order, Contact, UserProfile


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'category', 'transmission', 'price', 'is_available', 'seating_capacity', 'fuel_type')
    list_filter = ('category', 'is_available', 'fuel_type', 'transmission')
    search_fields = ('car_name', 'car_desc')
    list_editable = ('price', 'is_available')
    fieldsets = (
        ('Basic', {'fields': ('car_name', 'car_desc', 'price', 'image')}),
        ('Specs', {'fields': ('category', 'seating_capacity', 'fuel_type', 'transmission', 'mileage_kmpl', 'year')}),
        ('Status', {'fields': ('is_available',)}),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'car_name', 'user', 'days_for_rent', 'total_price', 'payment_status', 'pickup_date', 'created_at')
    list_filter = ('payment_status', 'city', 'pickup_date')
    search_fields = ('name', 'email', 'car_name', 'order_id')
    readonly_fields = ('created_at',)
    date_hierarchy = 'pickup_date'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city')
    search_fields = ('user__username', 'phone')
