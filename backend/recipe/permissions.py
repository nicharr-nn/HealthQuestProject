from rest_framework import permissions

class CanViewRecipe(permissions.BasePermission):
    """
    Allow:
    - Admins (staff or superuser)
    - Users with admin role
    - Coaches
    - Silver or Gold level users
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Staff or superuser
        if request.user.is_staff or request.user.is_superuser:
            return True

        profile = getattr(request.user, "userprofile", None)
        if profile is None:
            return False

        # Admin role
        if profile.role == "admin":
            return True

        # Coach role
        if profile.role == "coach":
            return True

        # Silver or Gold level
        level = profile.get_current_level().level
        return level in ["Silver", "Gold"]
