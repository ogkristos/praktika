from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from home.models import UserProfile  # Make sure this import is correct

class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                request.user.userprofile
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(
                    user=request.user,
                    profession=_('Other'),
                    Savings=0,
                    income=0
                )
        response = self.get_response(request)
        return response

class WordByWordTranslationMiddleware:
    """Middleware to ensure every word on the page is translated."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        return response

