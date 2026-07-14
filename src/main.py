"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


# --- Normal profiles: expected, "sane" taste combinations ---
NORMAL_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.95},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.90},
}

# --- Adversarial / edge case profiles: designed to try to break scoring ---
EDGE_CASE_PROFILES = {
    "Conflicting: Sad + High Energy": {"genre": "metal", "mood": "sad", "energy": 0.90},
    "Out-of-range energy target": {"genre": "jazz", "mood": "relaxed", "energy": 1.50},
    "Nonexistent genre": {"genre": "vaporwave", "mood": "happy", "energy": 0.50},
    "Sparse profile (mood only)": {"mood": "happy"},
}


def print_table(recommendations: list) -> None:
    """Prints recommendations as a formatted table including title, artist, score, and reasons."""
    rows = []
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        rows.append([
            rank,
            song["title"],
            song["artist"],
            f"{score:.2f}",
            "; ".join(reasons),
        ])

    headers = ["#", "Title", "Artist", "Score", "Reasons"]

    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="grid", maxcolwidths=[3, 18, 16, 6, 50]))
    else:
        # Simple ASCII fallback if tabulate isn't installed.
        widths = [3, 20, 16, 6, 60]
        header_line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
        print(header_line)
        print("-" * len(header_line))
        for row in rows:
            line = " | ".join(str(cell).ljust(w) for cell, w in zip(row, widths))
            print(line)


def run_profile(name: str, user_prefs: dict, songs: list) -> None:
    """Runs and prints the top 5 recommendations for a single user profile as a table."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 60)
    print(f"PROFILE: {name}")
    print(f"Preferences: {user_prefs}")
    print("=" * 60 + "\n")

    if not recommendations:
        print("(no recommendations met the minimum score threshold)\n")
        return

    print_table(recommendations)
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