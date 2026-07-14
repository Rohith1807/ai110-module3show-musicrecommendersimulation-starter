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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
  Each Song uses: genre (categorical), valence (0–1, sad↔happy), danceability (0–1), and one energy-axis feature — either energy or acousticness (only one, since they're near-mirror images of each other and including both would double-count the same signal). artist is also stored, used only for a small affinity bonus, not as a core similarity feature. tempo_bpm and mood are optional/secondary — tempo_bpm only if scaled to 0–1 first, and mood is left out of the core vector since it overlaps conceptually with valence/energy. title is stored for display only, not used in scoring.

- What information does your `UserProfile` store
  The UserProfile stores a preferred value for each numeric feature (e.g. preferred valence, preferred danceability, preferred energy) — either set explicitly or computed as the average of songs the user has liked. It also stores a set of preferred genres, a set of artists the user has liked, and a history/list of songs already played or liked (used later to exclude repeats from recommendations).

- How does your `Recommender` compute a score for each song
  For each numeric feature, it computes a closeness score using a scoring rule (e.g. 1 - abs(candidate_value - preferred_value) / range, or a Gaussian falloff), so songs close to the user's preferred value score highest in both directions rather than just "higher is better." It adds a genre match score (1 if the song's genre is in the user's preferred genres, else 0) and a small artist-affinity bonus if the song shares an artist with something the user liked. These components are combined into one final score using weights (e.g. score = w1*valence_score + w2*danceability_score + w3*energy_score + w4*genre_match + artist_bonus).

- How do you choose which songs to recommend
  This is the ranking rule: compute the final score for every candidate song, exclude songs already in the user's history, sort the remaining songs by score in descending order, and return the top N. Optional refinements include a minimum score cutoff (don't recommend anything below a threshold) and a diversity cap (avoid returning too many songs from the same artist or genre even if they all score well).

You can include a simple diagram or bullet list if helpful.

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



