# from django.urls import path
# # from . import views
# from .views import current_user_view, set_role_view, set_about_you, update_profile


# urlpatterns = [
#     path("user/", current_user_view, name="current-user"),
#     path("select-role/", set_role_view, name="select-role"),
#     path("set-about-you/", set_about_you, name="set-about-you"),
#     path("user/", current_user_view, name="current-user"),
#     path("update-profile/", update_profile, name="update-profile"),
# ]

from django.urls import path
from . import mock_views   # import from mock_views.py


urlpatterns = [
    path("mock-user/", mock_views.dev_mock_user, name="mock-user"),
]

