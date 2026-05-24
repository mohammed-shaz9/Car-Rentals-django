from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Car, Order, Contact, UserProfile

def index(request):
    featured_cars = Car.objects.filter(is_available=True)[:6]
    return render(request, 'index.html', {'featured_cars': featured_cars})

def about(request):
    return render(request, 'about.html')

def vehicles(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'vehicles.html', {'car': cars})

def car_list(request):
    category = request.GET.get('category', '')
    if category:
        cars = Car.objects.filter(category__iexact=category, is_available=True)
    else:
        cars = Car.objects.filter(is_available=True)
    return render(request, 'vehicles.html', {'car': cars})

def register(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('number', '')
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

        UserProfile.objects.create(user=user, phone=phone)

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
    cars = Car.objects.filter(is_available=True)
    selected_car = None
    car_name = request.GET.get('car_name', '')
    if car_name:
        selected_car = Car.objects.filter(car_name=car_name, is_available=True).first()

    if request.method == "POST":
        billname = request.POST.get('billname', '')
        billemail = request.POST.get('billemail', '')
        billphone = request.POST.get('billphone', '')
        billaddress = request.POST.get('billaddress', '')
        billcity = request.POST.get('billcity', '')
        car_id = request.POST.get('car_id', '')
        dayss = request.POST.get('dayss', '')
        date = request.POST.get('date', '')
        fl = request.POST.get('fl', '')
        tl = request.POST.get('tl', '')

        car = get_object_or_404(Car, id=car_id)
        days = int(dayss)
        total = car.price * days

        new_order = Order(
            user=request.user,
            name=billname,
            email=billemail,
            phone=billphone,
            address=billaddress,
            city=billcity,
            car=car,
            car_name=car.car_name,
            days_for_rent=days,
            price_per_day=car.price,
            total_price=total,
            date=date,
            loc_from=fl,
            loc_to=tl,
        )
        new_order.save()

        try:
            html_content = render_to_string('email_booking_confirmation.html', {
                'name': billname,
                'car_name': car.car_name,
                'days': days,
                'date': date,
                'loc_from': fl,
                'loc_to': tl,
                'total': total,
                'price_per_day': car.price,
            })
            text_content = strip_tags(html_content)
            email_msg = EmailMultiAlternatives(
                subject='Booking Confirmed - NovaFleet',
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[billemail],
            )
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send(fail_silently=False)
        except Exception as e:
            print(f"Email error: {e}")

        messages.success(request, "Booking confirmed! Check your email for details.")
        return redirect('confirm_booking')

    return render(request, 'bill.html', {
        'cars': cars,
        'selected_car': selected_car,
    })

@login_required(login_url='signin')
def confirm_booking(request):
    booking = Order.objects.filter(user=request.user).last()
    return render(request, 'confirm_booking.html', {'booking': booking})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('contactname', '')
        email = request.POST.get('contactemail', '')
        phone_number = request.POST.get('contactphone', '')
        message = request.POST.get('contactmsg', '')

        contact_entry = Contact(name=name, email=email, phone_number=phone_number, message=message)
        contact_entry.save()

        try:
            send_mail(
                subject=f'New Contact Form Message from {name}',
                message=f'Name: {name}\nEmail: {email}\nPhone: {phone_number}\nMessage: {message}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')
