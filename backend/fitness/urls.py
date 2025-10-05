from django.urls import path

from . import views

urlpatterns = [
    path("select-goal/", views.set_goal, name="select-goal"),
]
