import json
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import Q
from .models import Car, Order, Contact, UserProfile
from .forms import RegisterForm, LoginForm, BookingForm, ContactForm, UserProfileForm


def _send_html_email(subject, template, context, to_email):
    try:
        html = render_to_string(template, context)
        text = strip_tags(html)
        msg = EmailMultiAlternatives(subject, text, settings.EMAIL_HOST_USER, [to_email])
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def index(request):
    featured = Car.objects.filter(is_available=True)[:6]
    return render(request, 'index.html', {'featured_cars': featured})


def about(request):
    return render(request, 'about.html')


def vehicles(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'vehicles.html', {'car': cars})


def car_list(request):
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '')

    cars = Car.objects.filter(is_available=True)

    if q:
        cars = cars.filter(Q(car_name__icontains=q) | Q(car_desc__icontains=q))
    if category:
        cars = cars.filter(category__iexact=category)
    if min_price:
        cars = cars.filter(price__gte=min_price)
    if max_price:
        cars = cars.filter(price__lte=max_price)
    if sort == 'price_low':
        cars = cars.order_by('price')
    elif sort == 'price_high':
        cars = cars.order_by('-price')
    elif sort == 'name':
        cars = cars.order_by('car_name')

    return render(request, 'vehicles.html', {'car': cars, 'query': q})


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_available=True)
    similar = Car.objects.filter(category=car.category, is_available=True).exclude(id=car.id)[:3]
    return render(request, 'car_detail.html', {'car': car, 'similar': similar})


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            user = User.objects.create_user(username=d['username'], email=d['email'], password=d['password'])
            user.first_name = d['name']
            user.save()
            UserProfile.objects.create(user=user, phone=d['phone'])
            messages.success(request, "Account created! Please login.")
            return redirect('signin')
    return render(request, 'register.html', {'form': form})


def signin(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            messages.error(request, "Invalid credentials!")
    return render(request, 'login.html', {'form': form})


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

    initial = {
        'name': request.user.get_full_name() or '',
        'email': request.user.email,
        'phone': getattr(request.user.profile, 'phone', ''),
        'address': getattr(request.user.profile, 'address', ''),
        'city': getattr(request.user.profile, 'city', ''),
        'car': selected_car,
    }
    form = BookingForm(initial=initial)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            car = d['car']
            days = d['days_for_rent']
            discount = 0
            if days >= 7:
                discount = 0.10
            elif days >= 3:
                discount = 0.05
            total = int(car.price * days * (1 - discount))

            order = Order(
                user=request.user, name=d['name'], email=d['email'], phone=d['phone'],
                address=d['address'], city=d['city'], car=car, car_name=car.car_name,
                days_for_rent=days, price_per_day=car.price, total_price=total,
                pickup_date=d['pickup_date'], loc_from=d['loc_from'], loc_to=d['loc_to'],
            )
            order.save()

            _send_html_email(
                'Booking Confirmed - NovaFleet',
                'email_booking_confirmation.html',
                {'name': d['name'], 'car_name': car.car_name, 'days': days,
                 'date': str(d['pickup_date']), 'loc_from': d['loc_from'],
                 'loc_to': d['loc_to'], 'total': total, 'price_per_day': car.price,
                 'order_id': order.order_id, 'discount': int(discount * 100)},
                d['email']
            )

            messages.success(request, "Booking confirmed! Check your email.")
            return redirect('confirm_booking')

    return render(request, 'bill.html', {'form': form, 'cars': cars, 'selected_car': selected_car})


@login_required(login_url='signin')
def confirm_booking(request):
    booking = Order.objects.filter(user=request.user).select_related('car').last()
    return render(request, 'confirm_booking.html', {'booking': booking})


@login_required(login_url='signin')
def my_bookings(request):
    bookings = Order.objects.filter(user=request.user).select_related('car')
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required(login_url='signin')
def cancel_booking(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    if order.payment_status == 'confirmed':
        order.payment_status = 'cancelled'
        order.save()
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.error(request, "This booking cannot be cancelled.")
    return redirect('my_bookings')


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            d = form.cleaned_data
            send_mail(
                f'New Contact: {d["name"]}',
                f'Name: {d["name"]}\nEmail: {d["email"]}\nPhone: {d.get("phone_number", "")}\nMessage: {d["message"]}',
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=True,
            )
            messages.success(request, "Message sent successfully!")
            return redirect('contact')
    return render(request, 'contact.html', {'form': form})


@login_required(login_url='signin')
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = request.POST.get('name', request.user.first_name)
            request.user.save()
            messages.success(request, "Profile updated!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile_user': request.user})
