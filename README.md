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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
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



