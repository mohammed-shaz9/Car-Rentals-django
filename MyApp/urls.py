from django.urls import path
from MyApp import views

urlpatterns = [
    path("", views.index, name='home'),
    path("home", views.index, name='home'),
    path("about", views.about, name='about'),
    path("vehicles", views.vehicles, name="vehicles"),
    path("cars", views.car_list, name="cars"),
    path("car/<int:car_id>/", views.car_detail, name="car_detail"),
    path("register", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("bill", views.order, name="bill"),
    path("bookings", views.my_bookings, name="my_bookings"),
    path("booking/<int:order_id>/cancel", views.cancel_booking, name="cancel_booking"),
    path("confirm_booking", views.confirm_booking, name="confirm_booking"),
    path("contact", views.contact, name='contact'),
    path("profile", views.profile, name='profile'),
]