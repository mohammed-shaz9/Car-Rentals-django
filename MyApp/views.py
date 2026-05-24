from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Car, Order, Contact

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def vehicles(request):
    cars = Car.objects.all()
    return render(request, 'vehicles.html', {'car': cars})

def car_list(request):
    category = request.GET.get('category', '')
    if category:
        cars = Car.objects.filter(car_desc__icontains=category)
    else:
        cars = Car.objects.all()
    return render(request, 'vehicles.html', {'car': cars})

def register(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('signin')

    return render(request, 'register.html')

def signin(request):
    if request.method == "POST":
        loginusername = request.POST.get('loginusername', '')
        loginpassword = request.POST.get('loginpassword', '')
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return redirect('signin')

    return render(request, 'login.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

@login_required(login_url='signin')
def order(request):
    if request.method == "POST":
        billname = request.POST.get('billname', '')
        billemail = request.POST.get('billemail', '')
        billphone = request.POST.get('billphone', '')
        billaddress = request.POST.get('billaddress', '')
        billcity = request.POST.get('billcity', '')
        cars11 = request.POST.get('cars11', '')
        dayss = request.POST.get('dayss', '')
        date = request.POST.get('date', '')
        fl = request.POST.get('fl', '')
        tl = request.POST.get('tl', '')

        new_order = Order(
            name=billname,
            email=billemail,
            phone=billphone,
            address=billaddress,
            city=billcity,
            cars=cars11,
            days_for_rent=dayss,
            date=date,
            loc_from=fl,
            loc_to=tl
        )
        new_order.save()

        try:
            send_mail(
                subject='Booking Confirmed - NovaFleet',
                message=f'Dear {billname},\n\nYour booking for {cars11} has been confirmed!\n\nDetails:\nCar: {cars11}\nDays: {dayss}\nPickup Date: {date}\nFrom: {fl}\nTo: {tl}\nTotal: ₹{int(dayss) * 1000}\n\nThank you for choosing NovaFleet!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[billemail],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, "Booking confirmed! Check your email for details.")
        return redirect('confirm_booking')

    return render(request, 'bill.html')

@login_required(login_url='signin')
def confirm_booking(request):
    booking = Order.objects.filter(email=request.user.email).last()
    car = Car.objects.filter(car_name=booking.cars).first() if booking else None
    customer = {
        'name': booking.name,
        'email': booking.email,
        'phone': booking.phone
    } if booking else None
    return render(request, 'confirm_booking.html', {'booking': booking, 'car': car, 'customer': customer})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('contactname', '')
        email = request.POST.get('contactemail', '')
        message = request.POST.get('contactmsg', '')

        contact_entry = Contact(name=name, email=email, message=message)
        contact_entry.save()

        try:
            send_mail(
                subject=f'New Contact Form Message from {name}',
                message=f'Name: {name}\nEmail: {email}\nMessage: {message}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')
