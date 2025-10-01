from django.test import TestCase
import pytest
from users.models import User, UserProfile, UserLevel

@pytest.fixture
def gold_user(db):
    user = User.objects.create_user(username="goldtest", password="123456")
    profile = user.userprofile
    UserLevel.objects.create(user_profile=profile, level="Gold", level_rank=3, xp=6000)
    return user

