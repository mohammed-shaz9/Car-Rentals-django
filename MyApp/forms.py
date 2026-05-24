from django import forms
from django.contrib.auth.models import User
from .models import Car, Order, Contact, UserProfile


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, label='Full Name')
    username = forms.CharField(max_length=100, label='Username')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, required=False, label='Phone')
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address', 'city', 'car', 'days_for_rent', 'pickup_date', 'loc_from', 'loc_to']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date', 'min': ''}),
            'car': forms.Select(attrs={'onchange': 'updateCarPrice()'}),
            'days_for_rent': forms.NumberInput(attrs={'min': 1, 'max': 30, 'oninput': 'calculateTotal()'}),
            'address': forms.TextInput(),
            'loc_from': forms.TextInput(attrs={'placeholder': 'e.g., Hyderabad Airport'}),
            'loc_to': forms.TextInput(attrs={'placeholder': 'e.g., Hitech City'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(is_available=True)
        self.fields['car'].label_from_instance = lambda obj: f"{obj.car_name} - \u20b9{obj.price}/day"
        self.fields['days_for_rent'].label = 'Days'
        self.fields['pickup_date'].label = 'Pickup Date'
        self.fields['loc_from'].label = 'From Location'
        self.fields['loc_to'].label = 'To Location'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Your Phone'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city']
