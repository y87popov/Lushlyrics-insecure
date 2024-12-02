# main/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RestrictAnonymousAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = [reverse('login'), reverse('signup')]  # Adjust paths as needed
        if not request.user.is_authenticated and request.path not in allowed_urls:
            return redirect('login')
        return self.get_response(request)
