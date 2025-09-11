from django.urls import path
from .views import select_goal

urlpatterns = [
    path('select-goal/', select_goal, name='select-goal'),
]