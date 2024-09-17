from django.contrib import admin
from .models import Category, JobPosting, Application,UserProfile

admin.site.register(Category)

admin.site.register(JobPosting)

admin.site.register(Application)

admin.site.register(UserProfile)