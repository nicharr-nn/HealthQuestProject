from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile


class Command(BaseCommand):
    help = "Set admin role for all superusers"

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if profile.role != "admin":
                profile.role = "admin"
                profile.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Set admin role for {user.username}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"{user.username} already has admin role")
                )
