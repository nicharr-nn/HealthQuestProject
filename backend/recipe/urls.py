from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe-list'),
    path('<int:id>/', views.recipe_detail, name='recipe-detail'),
    path('<int:id>/download-pdf/', views.download_recipe_pdf, name='download-recipe-pdf'),
]
