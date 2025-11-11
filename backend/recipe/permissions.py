from rest_framework import permissions


class CanViewRecipe(permissions.BasePermission):
    """
    Allow:
    - Admins
    - Gold or Silver level users
    - Coaches
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Allow admins and staff
        if request.user.is_staff or request.user.is_superuser:
            return True

        profile = request.user.userprofile

        # Allow admin role
        if profile.role == "admin":
            return True

        if profile.role == "coach":
            return True

        level = profile.get_current_level().level
        return level in ["Silver", "Gold"]
