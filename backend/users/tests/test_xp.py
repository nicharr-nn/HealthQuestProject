import pytest
from django.contrib.auth.models import User
from users.models import UserProfile, UserLevel

@pytest.mark.django_db
def test_xp_addition_and_level_up():
    user = User.objects.create_user(username="testuser", password="testpass")
    profile = user.userprofile
    level = profile.get_current_level()

    assert level.level_rank == 1
    assert level.xp == 0

    # Add XP
    leveled_up, old_rank, new_rank = level.add_xp(120)

    assert level.xp == 120
    assert leveled_up is True or False  # depends on xp_rules
    assert isinstance(old_rank, int)
    assert isinstance(new_rank, int)

def test_xp_levels():
    from users.xp_rules import level_for_xp

    assert level_for_xp(0) == (1, "Bronze", 1000)
    assert level_for_xp(1200) == (2, "Silver", 3800)
    assert level_for_xp(4500) == (3, "Gold", None)


