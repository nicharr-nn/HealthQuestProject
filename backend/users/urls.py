from django.urls import path
from . import mock_views, views 


urlpatterns = [
    path("mock-user/", mock_views.dev_mock_user, name="mock-user"),
    path('user-info/', views.user_info, name='user-info'),
    path('select-role/', views.set_role, name='select-role'),
    path('update-profile/', views.update_profile, name='update-profile'),
    
]

