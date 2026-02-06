from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('contactname')
        email = request.POST.get('contactemail')
        message = request.POST.get('contactmsg')
        
        try:
            # For debugging
            print(f"Attempting to send email from {email}")
            
            send_mail(
                subject=f'New Contact Form Message from {name}',
                message=f'Name: {name}\nEmail: {email}\nMessage: {message}',
                from_email=EMAIL_HOST_USER,
                recipient_list=['carrentals047@gmail.com'],
                fail_silently=False,
            )
            print("Email sent successfully")  # Debug print
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        except Exception as e:
            print(f"Email error: {str(e)}")  # This will show the error in console
            messages.error(request, 'Failed to send message. Please try again.')
    
    return render(request, 'contact.html')


def bill(request):
    selected_car = request.GET.get('selected_car')
    if not selected_car:
        return redirect('vehicles')  # Redirect if no car selected
    return render(request, 'bill.html', {'selected_car': selected_car})