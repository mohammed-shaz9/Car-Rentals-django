from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings

from .models import Car, Order, Contact

# Home Page
def index(request):
    # Check if superuser exists, if not create one
    if not User.objects.filter(is_superuser=True).exists():
        try:
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("Superuser created successfully!")
        except Exception as e:
            print(f"Error creating superuser: {str(e)}")
    
    return render(request, 'index.html')

# About Page
def about(request):
    return render(request, 'about.html')

# Register Page
def register(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        number = request.POST.get('number', '')  # Currently unused
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Print debug information
        print(f"Registration attempt - Username: {username}, Email: {email}, Password length: {len(password)}")

        # Validate input data
        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('register')
        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        
        try:
            # Create user with proper error handling
            myuser = User.objects.create_user(username=username, email=email, password=password)
            myuser.first_name = name  # Using first_name since name doesn't exist in default User
            myuser.save()
            
            # Authenticate and log in the user immediately
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Your account has been successfully created and you are now logged in!")
                return redirect('vehicles')
            else:
                messages.success(request, "Your account has been successfully created! You can now login.")
                return redirect('signin')
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('register')
    else:
        return render(request, 'register.html')

# Login Page
def signin(request):
    # DIRECT LOGIN BYPASS
    # DIRECT LOGIN BYPASS
    try:
        user = User.objects.get(username='testuser')
        print("Test user already exists. Logging in...")
    except User.DoesNotExist:
        print("Test user does not exist. Creating test user...")
        user = User.objects.create_user(username='testuser', email='test@example.com', password='test123')
        user.save()
        messages.success(request, "Test user created successfully!")

    login(request, user)
    messages.success(request, "Login successful!")
    print("LOGGED IN SUCCESSFULLY WITH TEST USER")
    return redirect('vehicles')

# Logout
def signout(request):
    logout(request)
    return redirect('home')

# All Vehicles Page
def vehicles(request):
    cars = Car.objects.all()
    return render(request, 'vehicles.html', {'car': cars})

# Car Filtering by Category (Luxury, SUV, Pickup Truck)
def car_list(request):
    category = request.GET.get('category')

    if category == 'luxury':
        cars = Car.objects.filter(category='Luxury')
    elif category == 'suv':
        cars = Car.objects.filter(category='SUV')
    elif category == 'pickup':
        cars = Car.objects.filter(category='Pickup Truck')
    else:
        cars = Car.objects.all()

    return render(request, 'cars.html', {'car': cars})

# Bill Page
def bill(request):
    cars = Car.objects.all()
    return render(request, 'bill.html', {'cars': cars})

# Confirm Booking - Save Order
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
        return render(request, 'confirm_booking.html')
    else:
        return render(request, 'bill.html')

# Contact Form with Email Sending
def contact(request):
    if request.method == "POST":
        name = request.POST.get('contactname')
        email = request.POST.get('contactemail')
        phone = request.POST.get('contactnumber')
        message = request.POST.get('contactmsg')

        email_message = f"""
        New Contact Form Submission:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """

        try:
            send_mail(
                subject='New Contact Form Submission',
                message=email_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')

    return render(request, 'contact.html')

# Confirmation Page – shows details of latest booking
def confirm_booking(request):
    booking = Order.objects.last()
    car = Car.objects.filter(car_name=booking.cars).first() if booking else None
    customer = {
        'name': booking.name,
        'email': booking.email,
        'phone': booking.phone
    } if booking else None

    return render(request, 'confirm_booking.html', {'booking': booking, 'car': car, 'customer': customer})
