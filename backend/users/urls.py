from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('select-role/', views.select_role, name='select_role'),
    path('complete-onboarding/', views.complete_onboarding, name='complete_onboarding'),
    path('role-choices/', views.role_choices, name='role_choices'),
]