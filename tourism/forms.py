from django import forms
from django.contrib.auth.models import User
from .models import Booking, ContactMessage, Destination, Package, NewsletterSubscriber, UserProfile

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control py-3',
        'placeholder': 'First Name',
        'required': True
    }))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control py-3',
        'placeholder': 'Last Name',
        'required': True
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control py-3',
        'placeholder': 'Email Address',
        'required': True
    }))
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control py-3',
        'placeholder': 'Phone Number (Optional)'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-3',
        'placeholder': 'Create Password',
        'required': True
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-3',
        'placeholder': 'Confirm Password',
        'required': True
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control py-3',
                'placeholder': 'Choose Username',
                'required': True
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-3',
        'placeholder': 'Username or Email',
        'required': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-3',
        'placeholder': 'Password',
        'required': True
    }))


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'bio', 'passport_number', 'avatar']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 8900'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Falcon Way, New York'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about your travel dreams...'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional Passport/ID'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'package', 'destination', 'num_guests', 'date_time', 'special_request']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-transparent text-white',
                'id': 'name',
                'placeholder': 'Full Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-transparent text-white',
                'id': 'email',
                'placeholder': 'Email Address',
                'required': True,
            }),
            'package': forms.Select(attrs={
                'class': 'form-select bg-transparent text-white',
                'id': 'packageSelect',
            }),
            'destination': forms.Select(attrs={
                'class': 'form-select bg-transparent text-white',
                'id': 'destinationSelect',
            }),
            'num_guests': forms.NumberInput(attrs={
                'class': 'form-control bg-transparent text-white',
                'id': 'numGuests',
                'min': '1',
                'max': '20',
                'value': '1',
                'required': True,
            }),
            'date_time': forms.TextInput(attrs={
                'class': 'form-control bg-transparent text-white datetimepicker-input',
                'id': 'datetime',
                'placeholder': 'Date & Time',
                'data-target': '#date3',
                'data-toggle': 'datetimepicker',
                'required': True,
            }),
            'special_request': forms.Textarea(attrs={
                'class': 'form-control bg-transparent text-white',
                'placeholder': 'Special Requests (e.g. Dietary, Extra Luggage, Accessibility)',
                'id': 'message',
                'style': 'height: 90px'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['package'].queryset = Package.objects.all()
        self.fields['package'].empty_label = "Select Package (Optional)"
        self.fields['destination'].queryset = Destination.objects.all()
        self.fields['destination'].empty_label = "Select Destination"
        self.fields['destination'].required = False

    def clean_num_guests(self):
        num_guests = self.cleaned_data.get('num_guests')

        if num_guests is None:
            return num_guests

        if num_guests < 1:
            raise forms.ValidationError(
                "Number of guests must be at least 1."
            )

        if num_guests > 20:
            raise forms.ValidationError(
                "Number of guests cannot exceed 20."
            )

        return num_guests

    def clean(self):
        cleaned_data = super().clean()

        package = cleaned_data.get('package')
        num_guests = cleaned_data.get('num_guests')

        if package and num_guests:
            if num_guests > package.available_slots:
                self.add_error(
                    'num_guests',
                    f"Only {package.available_slots} slot(s) are "
                    "available for this package."
                )

        return cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'id': 'id_name',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'id': 'id_email',
                'placeholder': 'name@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input',
                'id': 'id_phone',
                'type': 'tel',
                'placeholder': '+1 800 000 0000',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'input',
                'id': 'id_message',
                'placeholder': 'How can we help you plan your journey?',
                'required': True
            }),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control w-100 py-3 ps-4 pe-5',
                'placeholder': 'Your email',
                'required': True
            })
        }
