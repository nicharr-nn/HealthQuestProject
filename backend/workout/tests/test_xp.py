from .. import xp_rules as xr


def test_calculate_xp_defaults():
    # default: duration=30, difficulty='medium' (mult=2.0) -> 30 * 1 * 2 = 60
    assert xr.calculate_xp() == 60


def test_calculate_xp_difficulty_multipliers():
    assert xr.calculate_xp(duration=30, difficulty_level="easy") == 30
    assert xr.calculate_xp(duration=30, difficulty_level="medium") == 60
    assert xr.calculate_xp(duration=30, difficulty_level="hard") == 90


def test_calculate_xp_with_intensity_and_rounding():
    # 10 minutes, easy (mult=1.0), intensity 1.5 -> 10 * 1 * 1.5 = 15
    assert xr.calculate_xp(duration=10, difficulty_level="easy", intensity=1.5) == 15


def test_calculate_xp_non_negative():
    # negative duration should not produce negative XP
    assert xr.calculate_xp(duration=-10) == 0


def test_level_for_xp_boundaries_and_next_level():
    # Bronze start
    rank, name, needed = xr.level_for_xp(0)
    assert rank == 1 and name == "Bronze" and needed == 1000

    # just below Silver
    rank, name, needed = xr.level_for_xp(999)
    assert rank == 1 and name == "Bronze" and needed == 1

    # exactly Silver threshold
    rank, name, needed = xr.level_for_xp(1000)
    assert rank == 2 and name == "Silver" and needed == 4000

    # exactly Gold threshold -> no next level
    rank, name, needed = xr.level_for_xp(5000)
    assert rank == 3 and name == "Gold" and needed is None


def test_calculate_xp_with_streak_and_completion():
    xp = xr.calculate_xp(
        duration=30, difficulty_level="medium", streak=True, completed=True
    )
    # 30*2=60, +10% streak = 66, +500 completion = 566
    assert xp == 566


def test_invalid_difficulty_defaults_to_easy():
    assert xr.calculate_xp(duration=30, difficulty_level="unknown") == 30


# Run tests with pytest in backend directory:
# pytest workout/tests/test_xp.py
