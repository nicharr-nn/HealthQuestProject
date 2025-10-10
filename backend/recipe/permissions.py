from rest_framework import permissions

class CanViewRecipe(permissions.BasePermission):
    """
    Allow:
    - Gold or Silver level users
    - Coaches
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        profile = request.user.userprofile

        if profile.role == "coach":
            return True

        level = profile.get_current_level().level
        return level in ["Silver", "Gold"]
