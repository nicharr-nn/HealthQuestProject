from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.models import User


def dev_login(request):
    username = request.GET.get("username")

    if not username:
        return JsonResponse({"error": "username is required"}, status=400)

    try:
        user = User.objects.get(username=username)

        backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user, backend=backend)

        return JsonResponse(
            {
                "status": "logged_in",
                "username": username,
                "user_id": user.id,
                "email": user.email,
            }
        )
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
