from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Stores the song catalog this recommender will score against."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked by fit against the user's profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable reason for why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv and returns a list of song dicts with numeric fields converted."""
    print(f"Loading songs from {csv_path}...")

    # Columns that hold numeric data and need conversion.
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)  # copy so we can safely overwrite values

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

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song against user_prefs and returns the top k, highest score first."""
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]