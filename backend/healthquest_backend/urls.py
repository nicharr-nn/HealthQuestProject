from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf.urls.static import static
from django.conf import settings

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


def home_view(request):
    """Simple home page view that returns user info or login status"""
    if request.user.is_authenticated:
        return JsonResponse(
            {
                "message": "Login successful!",
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                },
            }
        )
    else:
        return JsonResponse({"message": "Please log in"})




urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", home_view, name="home"),
    path("api/", include("users.urls")),
    path("api/fitness/", include("fitness.urls")),
    path("api/workout/", include("workout.urls")),
    path("api/coach/", include("coach.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
