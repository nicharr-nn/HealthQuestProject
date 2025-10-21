from django.urls import path

from . import views

urlpatterns = [
    path("", views.food_posts, name="food-posts"),
    path("<int:id>/update/", views.food_post_update, name="food-post-update"),
    path(
        "<int:id>/upload-image/",
        views.upload_food_post_image,
        name="upload-food-post-image",
    ),
    path("<int:id>/delete/", views.food_post_delete, name="food-post-delete"),
]
