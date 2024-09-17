
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERNSHIP = 'Internship'
    
    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (CONTRACT, 'Contract'),
        (INTERNSHIP, 'Internship'),
    ]
    MALE = 'Male'
    FEMALE = 'Female'
    NONE = 'None'
    
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NONE, 'None'),
    ]
    category = models.ForeignKey(Category, related_name='job_posting', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location =models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES, default=FULL_TIME)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField()

    applicants = models.ManyToManyField(User, related_name='job_applications', blank=True)

    def __str__(self):
        return self.title



class Application(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'
    
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    job_posting = models.ForeignKey(JobPosting, related_name='application', on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    skills = models.TextField()
    education= models.CharField(max_length=255)
    experience = models.TextField()
    resume = models.FileField(upload_to='resumes/')
   
    resume_link = models.URLField(blank=True, null=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.applicant_name}'


        






from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


    
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

