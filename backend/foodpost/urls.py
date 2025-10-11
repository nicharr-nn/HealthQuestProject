from django.urls import path

from . import views

urlpatterns = [
    path("", views.food_posts, name="food-posts"),
    path("<int:id>/", views.food_post_update, name="food-post-update"),
]