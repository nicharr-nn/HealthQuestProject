from django.urls import path
from .views import coach_member_requests, accepted_members

urlpatterns = [
    path('coach-requests/', coach_member_requests, name='coach-member-requests'),
    path(
        'coach-requests/<int:pk>/',
        coach_member_requests,
        name='coach-member-requests-detail'
    ),
    path('accepted/', accepted_members, name='accepted-members')
]
