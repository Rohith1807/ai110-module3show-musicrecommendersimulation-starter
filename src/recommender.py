"""
Core logic for the Music Recommender Simulation.

Implements:
- load_songs
- score_song
- recommend_songs
"""

import csv
from typing import List, Dict, Tuple


def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv and returns a list of song dicts with numeric fields converted."""
    print(f"Loading songs from {csv_path}...")

    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)

            for field in int_fields:
                if field in song and song[field] != "":
                    song[field] = int(song[field])

            for field in float_fields:
                if field in song and song[field] != "":
                    song[field] = float(song[field])

            songs.append(song)

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against user_prefs and returns (score, list of reasons)."""
    reasons: List[str] = []
    score = 0.0

    # --- Genre match (+2.0) ---
    target_genre = user_prefs.get("genre")
    if target_genre and song.get("genre") == target_genre:
        score += 2.0
        reasons.append(f"genre matches '{target_genre}' (+2.0)")

    # --- Mood match (+1.0) ---
    target_mood = user_prefs.get("mood")
    if target_mood and song.get("mood") == target_mood:
        score += 1.0
        reasons.append(f"mood matches '{target_mood}' (+1.0)")

    # --- Energy closeness (up to +2.0) ---
    # Rewards songs whose energy is CLOSE to the target, not just higher.
    target_energy = user_prefs.get("energy")
    if target_energy is not None and "energy" in song:
        # Validate the target is within the valid 0-1 scale. Values outside
        # this range are clamped rather than silently producing a 0.00 score
        # with no indication anything was wrong upstream.
        if target_energy < 0.0 or target_energy > 1.0:
            reasons.append(
                f"warning: target_energy {target_energy:.2f} is outside "
                f"valid range [0.0, 1.0], clamped for scoring"
            )
            target_energy = max(0.0, min(1.0, target_energy))

        energy_range = 1.0  # energy is stored on a 0-1 scale
        distance = abs(song["energy"] - target_energy)
        closeness = max(0.0, 1 - distance / energy_range)
        energy_points = 2.0 * closeness
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {target_energy:.2f} "
            f"(+{energy_points:.2f})"
        )

    if not reasons:
        reasons.append("no matching criteria")

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    min_score: float = 0.01,
) -> List[Tuple[Dict, float, List[str]]]:
    """
    Scores every song against user_prefs and returns the top k, highest
    score first.

    min_score filters out songs that scored 0 (no real signal at all) so a
    sparse profile doesn't return arbitrary, order-of-insertion "matches"
    with nothing behind them. Set min_score=0.0 to disable filtering.
    """
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    scored = [item for item in scored if item[1] >= min_score]

    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]