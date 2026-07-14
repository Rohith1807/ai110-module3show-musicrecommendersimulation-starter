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
    """Reads songs.csv and returns a list of song dicts with numeric/typed fields converted."""
    print(f"Loading songs from {csv_path}...")

    int_fields = {"id", "tempo_bpm", "popularity"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}
    bool_fields = {"explicit_content"}

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

            for field in bool_fields:
                if field in song and song[field] != "":
                    song[field] = song[field].strip().lower() == "true"

            # mood_tags is stored as a semicolon-separated string in the CSV
            # (commas are already used as the CSV delimiter), so split it
            # into a list of individual tags for scoring.
            if "mood_tags" in song and song["mood_tags"]:
                song["mood_tags"] = [
                    tag.strip() for tag in song["mood_tags"].split(";") if tag.strip()
                ]
            else:
                song["mood_tags"] = []

            songs.append(song)

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores one song against user_prefs and returns (score, list of reasons).

    Core weights: genre +2.0, mood +1.0, energy closeness up to +2.0.

    Advanced attribute weights (new):
      - Popularity closeness: up to +1.0 (only if user_prefs has target_popularity)
      - Release decade match: +0.5
      - Mood tag overlap: +0.5 per matching tag, capped at +1.0
      - Vocal style match: +0.5
      - Explicit content filter: -2.0 penalty if user_prefs["avoid_explicit"]
        is True and the song is flagged explicit
    """
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
    target_energy = user_prefs.get("energy")
    if target_energy is not None and "energy" in song:
        if target_energy < 0.0 or target_energy > 1.0:
            reasons.append(
                f"warning: target_energy {target_energy:.2f} is outside "
                f"valid range [0.0, 1.0], clamped for scoring"
            )
            target_energy = max(0.0, min(1.0, target_energy))

        energy_range = 1.0
        distance = abs(song["energy"] - target_energy)
        closeness = max(0.0, 1 - distance / energy_range)
        energy_points = 2.0 * closeness
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {target_energy:.2f} "
            f"(+{energy_points:.2f})"
        )

    # --- Popularity closeness (up to +1.0) ---
    target_popularity = user_prefs.get("target_popularity")
    if target_popularity is not None and "popularity" in song:
        clamped_target = max(0, min(100, target_popularity))
        pop_range = 100.0
        distance = abs(song["popularity"] - clamped_target)
        closeness = max(0.0, 1 - distance / pop_range)
        pop_points = 1.0 * closeness
        score += pop_points
        reasons.append(
            f"popularity {song['popularity']} vs target {clamped_target} "
            f"(+{pop_points:.2f})"
        )

    # --- Release decade match (+0.5) ---
    target_decade = user_prefs.get("release_decade")
    if target_decade and song.get("release_decade") == target_decade:
        score += 0.5
        reasons.append(f"release decade matches '{target_decade}' (+0.5)")

    # --- Mood tag overlap (+0.5 per match, capped at +1.0) ---
    target_tags = user_prefs.get("mood_tags")
    if target_tags:
        song_tags = set(song.get("mood_tags", []))
        matched_tags = [tag for tag in target_tags if tag in song_tags]
        if matched_tags:
            tag_points = min(1.0, 0.5 * len(matched_tags))
            score += tag_points
            reasons.append(
                f"mood tags matched: {', '.join(matched_tags)} (+{tag_points:.2f})"
            )

    # --- Vocal style match (+0.5) ---
    target_vocal = user_prefs.get("vocal_style")
    if target_vocal and song.get("vocal_style") == target_vocal:
        score += 0.5
        reasons.append(f"vocal style matches '{target_vocal}' (+0.5)")

    # --- Explicit content filter (-2.0 penalty) ---
    if user_prefs.get("avoid_explicit") and song.get("explicit_content"):
        score -= 2.0
        reasons.append("penalized: marked explicit_content, user avoids explicit (-2.0)")

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

    min_score filters out songs that scored 0 or below (no real signal, or
    fully penalized by the explicit-content filter) so a sparse profile
    doesn't return arbitrary matches with nothing behind them. Set
    min_score to a very negative number to disable filtering.
    """
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    scored = [item for item in scored if item[1] >= min_score]

    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]