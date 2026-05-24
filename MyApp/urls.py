from django.urls import path
from MyApp import views

urlpatterns = [
    path("", views.index, name='home'),
    path("home", views.index, name='home'),
    path("about", views.about, name='about'),
    path("vehicles", views.vehicles, name="vehicles"),
    path("register", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("bill", views.order, name="bill"),
    path("cars", views.car_list, name="cars"),
    path("contact", views.contact, name='contact'),
]