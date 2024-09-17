from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class SuperuserAutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated and is a superuser
        if request.user.is_authenticated and request.user.is_superuser:
            # Set session expiry for superusers to 2 minutes (or any duration you prefer)
            expiry_time = timezone.now() + timedelta(minutes=2)
            request.session.set_expiry(expiry_time)

        return response
