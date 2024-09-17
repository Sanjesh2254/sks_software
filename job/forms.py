from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
        }



from django import forms
from .models import JobPosting, Category

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'category',
            'title',
            'description',
            'location',
            'gender',
            'job_type',
            'salary',
            'requirements',
            'application_deadline',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'salary': forms.NumberInput(attrs={'step': '0.01'}),
        }



from django import forms
from .models import Application

class ApplyForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            
            'applicant_name',
            'address',
            'email',
            'phone_number',
            'age',
            'gender',
            'skills',
            'education',
            'experience',
            'resume',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'experience': forms.Textarea(attrs={'rows': 4}),
            'education': forms.TextInput(attrs={'placeholder': 'e.g., Bachelor of Science'}),
            'resume': forms.ClearableFileInput(attrs={'multiple': False}),
            'age': forms.NumberInput(attrs={'min': 1, 'max': 120}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g., 1234567890'}),
        }



from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'full_name',
            'address',
            'phone_number',
            'age',
            'gender',
            'skills',
            'education',
            'experience',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'experience': forms.Textarea(attrs={'rows': 4}),
            'education': forms.TextInput(attrs={'placeholder': 'e.g., Bachelor of Science'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g., 123-456-7890'}),
            'age': forms.NumberInput(attrs={'min': 0}),
            'gender': forms.Select(choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
        }



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }
