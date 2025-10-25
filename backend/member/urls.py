from django.urls import path
from .views import *

urlpatterns = [
    path('coach-requests/', coach_member_requests, name='coach-member-requests'),
    path(
        'coach-requests/<int:pk>/',
        coach_member_requests,
        name='coach-member-requests-detail'
    ),
    path('accepted/', accepted_members, name='accepted-members'),

    # member specific endpoints
    path("member-apply/", apply_as_member, name="apply_as_member"),
    path("member-profile/", get_member_profile, name="get_member_profile"),
    path("member-request/manage/", manage_member_request, name="manage_member_request"),
]
