from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import DonorProfile, BloodRequest, BloodGroup, UrgencyLevel

class DonorRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
            'placeholder': 'John'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
            'placeholder': 'Doe'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
            'placeholder': 'john.doe@example.com'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
            'placeholder': 'johndoe'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
            'placeholder': '••••••••'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
            'placeholder': '••••••••'
        })
    )

    class Meta:
        model = DonorProfile
        fields = ['blood_group', 'phone', 'city', 'address', 'is_available', 'last_donated', 'bio']
        widgets = {
            'blood_group': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 bg-white transition'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': '+1 (555) 000-0000'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'New York, London, Dhaka, etc.'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'Neighborhood / Area / Postal code'
            }),
            'last_donated': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'Tell us about your donation experience, preferred time to donate, or any notes.'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-600 bg-gray-100 border-gray-300 rounded focus:ring-red-500'
            })
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
            'placeholder': '••••••••'
        })
    )


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            'patient_name', 'blood_group', 'units_needed', 'urgency',
            'hospital', 'hospital_address', 'location', 'contact_number',
            'alternate_contact', 'needed_by', 'notes'
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'Full name of the patient'
            }),
            'blood_group': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 bg-white transition'
            }),
            'units_needed': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'min': 1, 'max': 50
            }),
            'urgency': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 bg-white transition'
            }),
            'hospital': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'e.g. City General Hospital, Apollo, Mount Sinai'
            }),
            'hospital_address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'Ward 4B, Building 2, 123 Healthcare Ave'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'City, District or Region'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'Primary Phone / WhatsApp number'
            }),
            'alternate_contact': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'Backup Phone (Optional)'
            }),
            'needed_by': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'placeholder': 'Medical case (e.g. Surgery, Thalassemia, Accident), special instructions or donor criteria.'
            }),
        }


class DonorProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
        })
    )

    class Meta:
        model = DonorProfile
        fields = ['blood_group', 'phone', 'city', 'address', 'is_available', 'last_donated', 'total_donations', 'bio']
        widgets = {
            'blood_group': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 bg-white transition'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
            }),
            'total_donations': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition',
                'min': 0
            }),
            'last_donated': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-red-500 transition'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-600 bg-gray-100 border-gray-300 rounded focus:ring-red-500'
            })
        }
