"""
URL configuration for healthquest_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for healthquest_backend project.
"""
from django.contrib import admin
from django.urls import path, include 
from django.views.generic import TemplateView
from django.http import JsonResponse
from login_page import views

def home_view(request):
    """Simple home page view that returns user info or login status"""
    if request.user.is_authenticated:
        return JsonResponse({
            'message': 'Login successful!',
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        })
    else:
        return JsonResponse({'message': 'Please log in'})

def about_view(request):
    """About page view that returns user info and about message"""
    if request.user.is_authenticated:
        return JsonResponse({
            'message': 'Welcome to HealthQuest About Page!',
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        })
    else:
        return JsonResponse({'message': 'Please log in to access the about page'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("api/user-info/", views.user_info, name="user_info"),
    path('', home_view, name='home'),
    path('about/', about_view, name='about'), 
    path("api/", include("users.urls"))
]
