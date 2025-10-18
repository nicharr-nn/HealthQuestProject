from django.urls import path
from .views import coach_member_requests

urlpatterns = [
    path('coach-requests/', coach_member_requests, name='coach-member-requests'),
]