from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Car, Order as OrderModel, Contact

# ... (lines 10-123 kept as context, not replaced unless needed, but easier to just replace target blocks)

# Update order view to use OrderModel
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

        new_order = OrderModel(
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
        messages.success(request, "Booking confirmed!")
        return redirect('confirm_booking')
    else:
        return render(request, 'bill.html')

# ... (contact view skipped)

# Update confirm_booking view to use OrderModel
@login_required(login_url='signin')
def confirm_booking(request):
    # Only show orders for the logged-in user's email if possible
    booking = OrderModel.objects.filter(email=request.user.email).last()
    
    # Fallback if no matching email found (e.g. user entered different email)
    if not booking:
         pass

    car = Car.objects.filter(car_name=booking.cars).first() if booking else None
    customer = {
        'name': booking.name,
        'email': booking.email,
        'phone': booking.phone
    } if booking else None

    return render(request, 'confirm_booking.html', {'booking': booking, 'car': car, 'customer': customer})
