from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        """
        Redirect admins to /admin, other users to /select-role
        """
        user = request.user

        # Check if user is admin/staff
        if user.is_superuser or user.is_staff:
            return "http://127.0.0.1:5173/admin-user"

        # Check if user has admin role in profile
        if hasattr(user, "userprofile") and user.userprofile.role == "admin":
            return "http://127.0.0.1:5173/admin-user"

        # Default redirect for regular users
        return "http://127.0.0.1:5173/select-role"
