"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# --- Normal profiles: expected, "sane" taste combinations ---
NORMAL_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.95},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.90},
}

# --- Adversarial / edge case profiles: designed to try to break scoring ---
EDGE_CASE_PROFILES = {
    # Conflicting signal: sad mood paired with a very high energy target.
    # Real emotional conflict most songs won't satisfy on both axes at once.
    "Conflicting: Sad + High Energy": {"genre": "metal", "mood": "sad", "energy": 0.90},

    # Out-of-range target: energy target above the valid 0-1 scale.
    # Tests whether the closeness formula degrades gracefully or breaks.
    "Out-of-range energy target": {"genre": "jazz", "mood": "relaxed", "energy": 1.50},

    # Genre that doesn't exist anywhere in the dataset.
    # Tests whether scoring still falls back sensibly to mood + energy only.
    "Nonexistent genre": {"genre": "vaporwave", "mood": "happy", "energy": 0.50},

    # Sparse profile: missing genre and energy entirely.
    # Tests whether score_song handles missing keys without crashing.
    "Sparse profile (mood only)": {"mood": "happy"},
}


def run_profile(name: str, user_prefs: dict, songs: list) -> None:
    """Runs and prints the top 5 recommendations for a single user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 60)
    print(f"PROFILE: {name}")
    print(f"Preferences: {user_prefs}")
    print("=" * 60 + "\n")

    for rank, rec in enumerate(recommendations, start=1):
        song, score, reasons = rec
        print(f"{rank}. {song['title']} (by {song['artist']})")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"     - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("\n" + "#" * 60)
    print("# NORMAL PROFILES")
    print("#" * 60)
    for name, prefs in NORMAL_PROFILES.items():
        run_profile(name, prefs, songs)

    print("\n" + "#" * 60)
    print("# ADVERSARIAL / EDGE CASE PROFILES")
    print("#" * 60)
    for name, prefs in EDGE_CASE_PROFILES.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()