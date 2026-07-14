# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

## Overview
 
This system recommends songs to a user by comparing each song's features
against a `UserProfile` taste profile, computing a weighted point score for
every candidate, and returning a ranked list. It uses pure content-based
filtering — no collaborative data from other users.
 
## 1. Song features
 
Each `Song` uses:
 
- `genre` (categorical)
- `mood` (categorical, light-weight secondary signal)
- `energy` (0–1) *or* `acousticness` (0–1) — only one is used, since these
  two are near-mirror opposites and including both would double-count the
  same signal
- `valence` (0–1, sad ↔ happy)
- `danceability` (0–1)
- `artist` (used only for a small affinity bonus, not core similarity)
- `tempo_bpm` (optional, only if min-max scaled to 0–1 first)
- `title` (display only, not used in scoring)

## 2. User profile
 
The `UserProfile` stores:
 
```python
user_profile = {
    "favorite_genre": "lofi",
    "secondary_genres": ["ambient", "jazz"],
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_valence": 0.60,
    "target_danceability": 0.55,
    "favorite_artists": ["LoRoom", "Paper Lanterns"],
    "history": [2, 4, 9]
}
```
 
## 3. Finalized scoring rule (point-weighted)
 
| Component               | Max points | Rule                                                                 |
|--------------------------|-----------:|-----------------------------------------------------------------------|
| Genre match              | +2.0       | 2.0 if genre == favorite_genre; +1.0 if in secondary_genres; else 0    |
| Mood match               | +1.0       | +1.0 if mood == favorite_mood, else 0                                  |
| Energy similarity        | +2.0       | `2.0 * (1 - abs(energy - target_energy) / energy_range)`              |
| Valence similarity       | +1.5       | `1.5 * (1 - abs(valence - target_valence) / valence_range)`           |
| Danceability similarity  | +1.0       | `1.0 * (1 - abs(danceability - target_danceability) / dance_range)`   |
| Artist bonus             | +0.5       | +0.5 if artist is in favorite_artists                                  |
| **Max possible score**   | **8.0**    | Sum of all components                                                  |
 
```
score = genre_score + mood_score + energy_score + valence_score + dance_score + artist_bonus
```
 
Normalize with `score / 8.0` for a 0–1 range if needed.
 
### Why these weights
 
- Genre (2.0) and energy similarity (2.0) are the two dominant signals —
  together they're what cleanly separates something like "intense rock" from
  "chill lofi."
- Valence (1.5) is weighted just under genre/energy because it's the most
  independent numeric feature (least correlated with the others), so it adds
  real information rather than restating what energy already says.
- Danceability (1.0) is lighter because it's fairly correlated with energy —
  full weight would partially double-count that axis.
- Mood (1.0) is intentionally half of genre's weight. Mood tags often overlap
  with what the numeric features already encode (e.g. "chill" mood usually
  comes bundled with low energy + high acousticness), so mood is treated as a
  tiebreaker, not a primary driver.
- Artist bonus (0.5) is a small nudge, not enough to let a poor overall match
  win purely on artist loyalty.

## 4. Ranking rule
 
1. Compute the score for every candidate song.
2. Exclude songs already in `user_profile["history"]`.
3. Sort remaining songs by score, descending.
4. Return the top N.
5. Optional refinements: a minimum score threshold, or a diversity cap
   limiting how many results come from the same artist/genre.

## 5. Known / expected biases
 
- **Genre may overshadow mood-based fit.** Because genre carries double the
  weight of mood, a song that's a strong mood match but in an unlisted or
  non-favorite genre can rank below a song that's merely genre-correct but a
  weaker overall vibe match. *Example: this system might over-prioritize
  genre, ignoring a great song that matches the user's mood but sits in a
  different genre bucket.*
- **Single-genre credit is brittle.** A song in a genre adjacent to the
  favorite (e.g. "dream pop" next to "lofi") gets zero genre credit unless
  it's explicitly listed in `secondary_genres`, even if its numeric features
  are a near-perfect match.
- **Point targets, not ranges.** Numeric scoring rewards closeness to one
  exact target value. A user who's fine with "anything under 0.5 energy"
  isn't well represented — a song at energy 0.20 can score worse than one at
  0.40, even though both may be equally acceptable to the user.
- **No negative preferences.** The profile only encodes attraction, not
  aversion — there's no way to penalize a disliked genre or artist beyond it
  simply not matching the favorites list.
- **Cold-start / new-artist bias.** Since the artist bonus only fires for
  artists already in `favorite_artists`, new or undiscovered artists start
  with a built-in disadvantage relative to familiar ones, even with identical
  audio features.
- **Static profile.** The profile doesn't automatically update as the user
  likes or skips new songs; without a periodic recompute step, taste drift
  over time won't be reflected.


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output



```
Loading songs from data/songs.csv...

==================================================
TOP RECOMMENDATIONS
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
==================================================

1. Sunrise City (by Neon Echo)
   Score: 4.96
   Reasons:
     - genre matches 'pop' (+2.0)
     - mood matches 'happy' (+1.0)
     - energy 0.82 vs target 0.80 (+1.96)

2. Gym Hero (by Max Pulse)
   Score: 3.74
   Reasons:
     - genre matches 'pop' (+2.0)
     - energy 0.93 vs target 0.80 (+1.74)

3. Rooftop Lights (by Indigo Parade)
   Score: 2.92
   Reasons:
     - mood matches 'happy' (+1.0)
     - energy 0.76 vs target 0.80 (+1.92)

4. Streetlight Cypher (by MC Lumen)
   Score: 2.00
   Reasons:
     - energy 0.80 vs target 0.80 (+2.00)

5. Night Drive Loop (by Neon Echo)
   Score: 1.90
   Reasons:
     - energy 0.75 vs target 0.80 (+1.90)

==================================================

```

## Profile prefernce

```
Loading songs from data/songs.csv...
                                                                       
############################################################            
# NORMAL PROFILES                                                     
############################################################         
                                                                       
============================================================           
PROFILE: High-Energy Pop                                                   
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.95}
============================================================

1. Sunrise City (by Neon Echo)
   Score: 4.74
   Reasons:
     - genre matches 'pop' (+2.0)
     - mood matches 'happy' (+1.0)
     - energy 0.82 vs target 0.95 (+1.74)

2. Gym Hero (by Max Pulse)
   Score: 3.96
   Reasons:
     - genre matches 'pop' (+2.0)
     - energy 0.93 vs target 0.95 (+1.96)

3. Rooftop Lights (by Indigo Parade)
   Score: 2.62
   Reasons:
     - mood matches 'happy' (+1.0)
     - energy 0.76 vs target 0.95 (+1.62)

4. Neon Pulse Rising (by Kilowatt)
   Score: 2.00
   Reasons:
     - energy 0.95 vs target 0.95 (+2.00)

5. Iron Fist (by Grave Siren)
   Score: 1.96
   Reasons:
     - energy 0.97 vs target 0.95 (+1.96)


============================================================
PROFILE: Chill Lofi
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
============================================================

1. Library Rain (by Paper Lanterns)
   Score: 5.00
   Reasons:
     - genre matches 'lofi' (+2.0)
     - mood matches 'chill' (+1.0)
     - energy 0.35 vs target 0.35 (+2.00)

2. Midnight Coding (by LoRoom)
   Score: 4.86
   Reasons:
     - genre matches 'lofi' (+2.0)
     - mood matches 'chill' (+1.0)
     - energy 0.42 vs target 0.35 (+1.86)

3. Focus Flow (by LoRoom)
   Score: 3.90
   Reasons:
     - genre matches 'lofi' (+2.0)
     - energy 0.40 vs target 0.35 (+1.90)

4. Spacewalk Thoughts (by Orbit Bloom)
   Score: 2.86
   Reasons:
     - mood matches 'chill' (+1.0)
     - energy 0.28 vs target 0.35 (+1.86)

5. Coffee Shop Stories (by Slow Stereo)
   Score: 1.96
   Reasons:
     - energy 0.37 vs target 0.35 (+1.96)


============================================================
PROFILE: Deep Intense Rock
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
============================================================

1. Storm Runner (by Voltline)
   Score: 4.98
   Reasons:
     - genre matches 'rock' (+2.0)
     - mood matches 'intense' (+1.0)
     - energy 0.91 vs target 0.90 (+1.98)

2. Gym Hero (by Max Pulse)
   Score: 2.94
   Reasons:
     - mood matches 'intense' (+1.0)
     - energy 0.93 vs target 0.90 (+1.94)

3. Neon Pulse Rising (by Kilowatt)
   Score: 1.90
   Reasons:
     - energy 0.95 vs target 0.90 (+1.90)

4. Iron Fist (by Grave Siren)
   Score: 1.86
   Reasons:
     - energy 0.97 vs target 0.90 (+1.86)

5. Sunrise City (by Neon Echo)
   Score: 1.84
   Reasons:
     - energy 0.82 vs target 0.90 (+1.84)


############################################################
# ADVERSARIAL / EDGE CASE PROFILES
############################################################

============================================================
PROFILE: Conflicting: Sad + High Energy
Preferences: {'genre': 'metal', 'mood': 'sad', 'energy': 0.9}
============================================================

1. Iron Fist (by Grave Siren)
   Score: 3.86
   Reasons:
     - genre matches 'metal' (+2.0)
     - energy 0.97 vs target 0.90 (+1.86)

2. Storm Runner (by Voltline)
   Score: 1.98
   Reasons:
     - energy 0.91 vs target 0.90 (+1.98)

3. Gym Hero (by Max Pulse)
   Score: 1.94
   Reasons:
     - energy 0.93 vs target 0.90 (+1.94)

4. Neon Pulse Rising (by Kilowatt)
   Score: 1.90
   Reasons:
     - energy 0.95 vs target 0.90 (+1.90)

5. Sunrise City (by Neon Echo)
   Score: 1.84
   Reasons:
     - energy 0.82 vs target 0.90 (+1.84)


============================================================
PROFILE: Out-of-range energy target
Preferences: {'genre': 'jazz', 'mood': 'relaxed', 'energy': 1.5}
============================================================

1. Coffee Shop Stories (by Slow Stereo)
   Score: 3.74
   Reasons:
     - genre matches 'jazz' (+2.0)
     - mood matches 'relaxed' (+1.0)
     - warning: target_energy 1.50 is outside valid range [0.0, 1.0], clamped for scoring
     - energy 0.37 vs target 1.00 (+0.74)

2. Iron Fist (by Grave Siren)
   Score: 1.94
   Reasons:
     - warning: target_energy 1.50 is outside valid range [0.0, 1.0], clamped for scoring
     - energy 0.97 vs target 1.00 (+1.94)

3. Neon Pulse Rising (by Kilowatt)
   Score: 1.90
   Reasons:
     - warning: target_energy 1.50 is outside valid range [0.0, 1.0], clamped for scoring
     - energy 0.95 vs target 1.00 (+1.90)

4. Gym Hero (by Max Pulse)
   Score: 1.86
   Reasons:
     - warning: target_energy 1.50 is outside valid range [0.0, 1.0], clamped for scoring
     - energy 0.93 vs target 1.00 (+1.86)

5. Storm Runner (by Voltline)
   Score: 1.82
   Reasons:
     - warning: target_energy 1.50 is outside valid range [0.0, 1.0], clamped for scoring
     - energy 0.91 vs target 1.00 (+1.82)


============================================================
PROFILE: Nonexistent genre
Preferences: {'genre': 'vaporwave', 'mood': 'happy', 'energy': 0.5}
============================================================

1. Rooftop Lights (by Indigo Parade)
   Score: 2.48
   Reasons:
     - mood matches 'happy' (+1.0)
     - energy 0.76 vs target 0.50 (+1.48)

2. Sunrise City (by Neon Echo)
   Score: 2.36
   Reasons:
     - mood matches 'happy' (+1.0)
     - energy 0.82 vs target 0.50 (+1.36)

3. Velvet Whisper (by Nadia Cole)
   Score: 2.00
   Reasons:
     - energy 0.50 vs target 0.50 (+2.00)

4. Golden Hour Drive (by Cassette Kids)
   Score: 1.90
   Reasons:
     - energy 0.55 vs target 0.50 (+1.90)

5. Wildflower Path (by Sable & Wren)
   Score: 1.90
   Reasons:
     - energy 0.45 vs target 0.50 (+1.90)


============================================================
PROFILE: Sparse profile (mood only)
Preferences: {'mood': 'happy'}
============================================================

1. Sunrise City (by Neon Echo)
   Score: 1.00
   Reasons:
     - mood matches 'happy' (+1.0)

2. Rooftop Lights (by Indigo Parade)
   Score: 1.00
   Reasons:
     - mood matches 'happy' (+1.0)

```
**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



