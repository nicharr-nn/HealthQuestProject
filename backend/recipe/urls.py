from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe-list"),
    path("my-recipes/", views.my_recipes, name="my-recipes"),
    path("<int:pk>/", views.recipe_detail, name="recipe-detail"),
    path(
        "<int:id>/download-pdf/", views.download_recipe_pdf, name="download-recipe-pdf"
    ),
    path(
        "<int:id>/upload-image/", views.upload_recipe_image, name="upload-recipe-image"
    ),
    path("<int:id>/delete/", views.delete_recipe, name="delete-recipe"),
    path("<int:id>/update/", views.update_recipe, name="update-recipe"),
]
