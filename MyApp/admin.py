from django.contrib import admin
from .models import Car, Order, Contact, UserProfile


class CarAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'category', 'price', 'is_available', 'seating_capacity', 'fuel_type')
    list_filter = ('category', 'is_available', 'fuel_type')
    search_fields = ('car_name', 'car_desc')
    list_editable = ('price', 'is_available')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'name', 'email', 'days_for_rent', 'total_price', 'payment_status', 'date', 'created_at')
    list_filter = ('payment_status', 'city', 'date')
    search_fields = ('name', 'email', 'car_name', 'order_id')
    readonly_fields = ('created_at',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'message')
    search_fields = ('name', 'email')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city')


admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
