# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch is a small, transparent, content-based song recommender built for
a classroom simulation, not a production app. Given a simple preference
profile (a favorite genre, a favorite mood, and a target energy level), it
scores every song in a fixed catalog and returns a ranked top-k list with a
plain-language explanation for each result.

It assumes the user can express their taste as a short, structured
preference set rather than through years of listening history — there's no
learning from past behavior, no collaborative signal from other users, and
no updating over time. It's built for classroom exploration of how a
recommender's scoring and ranking rules work, not for real end users making
real listening decisions. It's best understood as a teaching tool for
recommender system design, not a deployed product.

---

## 3. How the Model Works

Think of every song as having a few dials on it: what genre it's filed
under, what mood it's tagged with, and how energetic it sounds on a scale
from calm to intense. The user tells the system what dial settings they
want — say, "pop," "happy," and "pretty high energy" — and the system checks
every song in the catalog against those three dials.

Genre and mood are yes/no checks: either the song matches what the user
asked for, or it doesn't. Energy works differently — instead of just
rewarding "more energy is always better," it rewards songs whose energy is
*close* to what the user asked for, in either direction. A user who wants
medium energy shouldn't get punished by a song that's medium energy just
because a louder song exists; closeness to the target is what earns points,
not raw intensity.

Each of these checks is worth a different number of points — genre and
energy are weighted more heavily than mood — and a song's total score is
just the sum of all three. The system then sorts every song by that score,
throws out anything that scored basically nothing, and hands back the top
few results along with a short list of reasons explaining exactly why each
one made the cut.

What changed from the starter logic: the starter code was empty stubs. We
built the CSV loading (with proper type conversion so energy and tempo are
usable numbers, not text), the actual point-based scoring formula described
above, the "closer is better" energy math (instead of a naive "bigger
number is better" rule), a minimum-score filter so completely unrelated
songs don't pad out the results, and a light validation step so an
impossible energy target (like 1.5 on a 0–1 scale) gets caught and clamped
instead of quietly producing a broken score.

---

## 4. Data

The catalog is small and hand-built for this simulation — 10 songs in the
core dataset (with an additional 9-song expansion drafted separately to
broaden genre coverage). Each song has: title, artist, genre, mood, energy,
tempo, valence (how happy/sad it sounds), danceability, and acousticness.

**Genres represented in the core 10-song set:** lofi (3), pop (2), rock (1),
ambient (1), jazz (1), synthwave (1), indie pop (1).
**Moods represented:** chill (3), happy (2), intense (2), relaxed (1),
moody (1), focused (1).

We added 9 more songs specifically to cover genres and moods missing from
the original set — country, metal, R&B, reggae, EDM, classical, folk, dream
pop, and hip hop, along with moods like nostalgic, angry, romantic, playful,
triumphant, melancholic, dreamy, and energetic.

Even with the expansion, musical taste is still thin here. There's no true
silence-adjacent ambient/drone material (energy stays above ~0.28 even in
the calmest tracks), nothing at true maximum intensity (nothing above
~0.93), and no representation of world music, electronic subgenres beyond
EDM/synthwave, or spoken-word/podcast-adjacent audio. The dataset is a
sketch of musical taste, not a real catalog — it's meant to be big enough to
test scoring logic, not big enough to satisfy an actual listener.

---

## 5. Strengths

The system works best for users whose taste is internally consistent — where
genre, mood, and energy all point in the same direction. "Chill Lofi"
(lofi genre, chill mood, low energy) is the clearest example: all three
lofi songs in the catalog are also tagged chill and low-energy, so the
system confidently and correctly surfaces them at the top with high scores.
Similarly, "Deep Intense Rock" correctly finds the one rock song in the
catalog and ranks it first because its genre, mood, and energy are all
"intense" flavored at once.

The "closer is better" energy scoring correctly captures the idea that a
target energy of 0.5 should reward songs near 0.5, not just the loudest
song available — this matched our intuition well when we tested a "Chill
Lofi" profile with target energy 0.35 and saw `Library Rain` (energy 0.35,
a perfect match) beat out louder lofi tracks, exactly as expected.

The explanation ("Reasons") output is also a genuine strength — because
every score is broken into genre/mood/energy contributions, a user (or a
grader) can see exactly why a song was recommended, rather than trusting a
black-box number.

---

## 6. Limitations and Bias

The system over-prioritizes genre-labeled songs from the most common genre
(lofi, 30% of the catalog) because genre carries double the point weight of
mood, so users who define their taste primarily by feel rather than genre
label get systematically under-scored even when a good mood/energy match
exists. This creates a filter bubble where lofi-genre users keep getting
confidently ranked results while mood-driven users get thinner, less certain
lists. Separately, because no song in the dataset has an energy value below
0.28 or above 0.93, users targeting the true extremes of the energy scale
are structurally unable to score well no matter how the weights are tuned —
the closeness math is fair, but the data simply can't serve them, which the
scoring rule has no way to detect or flag.

A related issue: when a user's genre and mood don't co-occur anywhere in the
catalog (e.g. asking for a "sad metal" song when no such combination
exists), the system silently falls back to scoring on whatever single
feature still has signal — usually energy alone — without ever telling the
user that half of what they asked for went completely unmatched. The
recommendation still looks confident and ranked, even though it's really
only satisfying one of three stated preferences.

---

## 7. Evaluation

### Which user profiles you tested

We tested three "normal" profiles representing distinct, internally
consistent tastes, plus four adversarial/edge-case profiles designed to try
to break the scoring logic:

**Normal profiles:**
- High-Energy Pop — `{genre: pop, mood: happy, energy: 0.95}`
- Chill Lofi — `{genre: lofi, mood: chill, energy: 0.35}`
- Deep Intense Rock — `{genre: rock, mood: intense, energy: 0.90}`

**Edge case profiles:**
- Conflicting: Sad + High Energy — `{genre: metal, mood: sad, energy: 0.90}`
- Out-of-range energy target — `{genre: jazz, mood: relaxed, energy: 1.50}`
- Nonexistent genre — `{genre: vaporwave, mood: happy, energy: 0.50}`
- Sparse profile (mood only) — `{mood: happy}`

### What you looked for in the recommendations

For each profile, we checked whether the #1 result actually made sense given
the stated preferences (right genre, right mood, energy close to the
target), whether the explanations ("Reasons") correctly justified the score,
and whether songs that clearly didn't fit still managed to sneak into the
top 5. For the edge cases specifically, we checked whether the system would
crash, silently break, or just quietly produce a worse (but still honest)
answer when given contradictory or invalid input.

### What surprised you

The biggest surprise was that changing the point weights (halving genre's
importance, doubling energy's) didn't change a single top-5 ranking across
any of the three normal profiles — only the raw scores shifted. Genre and
energy almost always "agree" on which song is best in this dataset, so
reweighting them didn't flip any outcomes. This told us the exact weights
matter less than we assumed; the dataset itself has more influence on the
results than our tuning does.

The second surprise was how the system behaves at the edges of the data it's
seen. No song in the catalog has energy below 0.28 or above 0.93, so a user
who wants something truly extreme is structurally unable to score well, no
matter how the math is tuned. The formula itself isn't broken — it's just
that the system never tells the user "we don't really have anything for you"
when this happens; it recommends its best available option anyway, silently.

### Simple tests or comparisons you ran

- **High-Energy Pop vs. Chill Lofi** — nearly no overlap in results, which
  makes sense since their energy targets (0.95 vs. 0.35) sit at opposite
  ends of the scale.
- **High-Energy Pop vs. Deep Intense Rock** — both want high energy, so their
  top songs overlap (`Gym Hero`, `Sunrise City`, `Storm Runner` appear in
  both), but the #1 pick differs based on each profile's genre/mood, which is
  exactly what should break the tie between two equally loud songs.
- **Chill Lofi vs. Nonexistent genre ("vaporwave")** — Chill Lofi gets three
  strong lofi matches up top; the vaporwave profile gets zero genre credit
  (no song is tagged vaporwave) and falls back to mood + energy only, landing
  on a pop song instead — a sensible fallback, but a sign the system will
  confidently recommend something outside the requested genre if that genre
  simply isn't in the catalog.
- **Sparse profile (mood only) vs. Conflicting (sad + high energy)** — the
  sparse profile still gets two honest mood-only matches; the conflicting
  profile gets no mood or genre credit at all (no metal song is tagged "sad")
  and its ranking becomes pure energy-chasing, surfacing a song whose mood
  ("intense") is the opposite of what was asked for. This shows that when a
  user's preferences don't co-occur anywhere in the real data, the system
  quietly narrows down to whichever single feature still has signal, without
  flagging that part of the request went unmet.

---

## 8. Future Work

- **Add more features to the profile**, like danceability and valence, and
  let users specify a range or tolerance for energy instead of a single
  exact target — right now, a user who's fine with "anything under 0.5"
  isn't well represented by a single point target.
- **Better explanations** — right now the reasons list raw point
  contributions ("+1.96"), which is useful for debugging but not very human.
  A friendlier version might say "this is louder and more upbeat than most
  songs like it" instead of showing the math directly.
- **Improve diversity in the top results** — nothing currently stops the top
  5 from being dominated by one artist or one sub-genre; a simple diversity
  cap (e.g. no more than 2 songs per artist) would make the recommendations
  feel less repetitive.
- **Handle more complex or contradictory tastes** — right now, a profile
  that asks for two things that don't coexist in the data (like "sad metal")
  just silently drops to whichever single feature still has signal. A more
  honest system would tell the user "we couldn't find a strong match for
  everything you asked" instead of presenting a confident top 5 regardless.
- **Grow and diversify the dataset itself** — many of the biases we found
  are really data problems, not logic problems (no truly extreme energy
  songs, uneven genre representation). A bigger, more balanced catalog would
  fix more of these issues than any amount of weight-tuning.

---

## 9. Personal Reflection

Building this made it clear that a recommender system is really two separate
problems wearing one trenchcoat: deciding how to *score* something, and
deciding what to *do* with those scores once you have them. It's tempting to
think the scoring formula is where all the "smarts" live, but our
weight-shift experiment showed that changing the formula didn't actually
change any results — the dataset itself was doing more of the work than our
carefully chosen point values were.

The most interesting discovery was how much bias can hide in a system that
is, on a line-by-line basis, doing exactly what it was told to do. Nothing
in the code is "wrong," but a lofi-loving user gets a noticeably more
confident experience than a user chasing an unusual mood/genre combination,
purely because of how the weights and the dataset happen to interact. That
changed how I think about recommendation apps in general — a lot of what
looks like "the algorithm doesn't get me" probably isn't a broken algorithm
at all, it's a catalog that never had enough of what that person actually
wanted, combined with a scoring system that has no way to say so out loud.