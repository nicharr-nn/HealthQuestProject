"""
XP rules and level thresholds.
Defines how many XP points are needed for each level and any special rules.
"""

# LEVELS = list of (rank, name, xp_threshold)
# threshold = minimum xp required to reach that level.
LEVELS = [
    (1, "Bronze", 0),
    (2, "Silver", 1000),
    (3, "Gold", 5000),
]

# difficulty multipliers
DIFFICULTY_MULTIPLIER = {
    "easy": 1.0,
    "medium": 5.0,
    "hard": 10.0,
}

def calculate_xp(duration: int = 30, difficulty_level: str = "medium", intensity: float = 1.0) -> int:
    """
    XP formula:
      base_xp_per_minute * duration * difficulty_multiplier * intensity
    Round to integer and return non-negative.
    """
    base_per_min = 1  # 1 XP per minute baseline
    try:
        mult = DIFFICULTY_MULTIPLIER.get(difficulty_level, 1.0)
        intensity_val = float(intensity) if intensity is not None else 1.0
    except Exception:
        mult = 1.0
        intensity_val = 1.0

    xp = int(round(duration * base_per_min * mult * intensity_val))
    return max(0, xp)

def level_for_xp(xp: int):
    """
    Given XP, return a tuple: (level_rank, level_name, xp_required_for_next_level).
    """
    xp = int(max(0, xp))
    current_level = LEVELS[0]
    next_level = None

    for i, (rank, name, threshold) in enumerate(LEVELS):
        if xp >= threshold:
            current_level = (rank, name, threshold)
            if i + 1 < len(LEVELS):
                next_level = LEVELS[i + 1]
        else:
            break

    rank, name, threshold = current_level

    if next_level:
        xp_needed = next_level[2] - xp
    else:
        xp_needed = None

    return rank, name, xp_needed