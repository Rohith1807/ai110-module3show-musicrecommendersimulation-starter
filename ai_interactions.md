# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---
## Challenge 1: Add Advanced Song Features
 
### Prompt used
 
> "Introduce 5 or more complex attributes to your dataset that are not
> currently present in the baseline data, such as Song Popularity (0-100),
> Release Decade, or Detailed Mood Tags (e.g., 'nostalgic,' 'aggressive,'
> 'euphoric'). Update both data/songs.csv and the scoring logic in
> src/recommender.py so scoring accounts for the new attributes."
 
### Summary of changes the AI generated
 
**New attributes added to `data/songs.csv`:**
- `popularity` (0-100 integer)
- `release_decade` (e.g. "2020s", "2010s", "2000s")
- `mood_tags` (multiple detailed tags per song, e.g. "nostalgic;peaceful" —
  semicolon-separated within the cell since commas are already the CSV
  delimiter)
- `vocal_style` (e.g. "instrumental", "male vocals", "female vocals", "mixed")
- `explicit_content` (boolean flag)
**Changes to `recommender.py`:**
- `load_songs` now converts `popularity` to `int`, `explicit_content` to
  `bool` (parsed from the string "True"/"False"), and splits `mood_tags`
  into a Python list on the semicolon delimiter.
- `score_song` gained five new optional scoring components, each only
  activating if the corresponding key is present in `user_prefs` (so
  existing profiles that don't mention these attributes are unaffected):
  - Popularity closeness — up to +1.0, using the same "closer is better"
    formula as energy, scaled to a 0-100 range instead of 0-1.
  - Release decade match — flat +0.5 if it matches exactly.
  - Mood tag overlap — +0.5 per matching tag, capped at +1.0 (so at most
    2 tags count toward the score).
  - Vocal style match — flat +0.5.
  - Explicit content filter — a -2.0 penalty if `user_prefs["avoid_explicit"]`
    is True and the song is flagged explicit, rather than a hard exclusion,
    so it still shows up in reasons if it's otherwise a strong match.
- New max possible score: 8.0 (up from 5.0), sum of genre 2.0 + mood 1.0 +
  energy 2.0 + popularity 1.0 + decade 0.5 + mood tags 1.0 + vocal style 0.5.
  
### Manual verification notes
 
- Ran a "perfect match" test (a profile matching every attribute of one
  specific song exactly) and confirmed the score hit exactly 8.0, the new
  theoretical max — confirms no double-counting or overflow in the added
  terms.
- Printed a loaded song dict directly and confirmed `popularity` was an
  `int`, `mood_tags` was a `list` (not a raw string), and `explicit_content`
  was a real `bool` — not just string values that happened to look right.
- Caught a **stale-file bug during testing**: an experimental weight-shifted
  copy of `recommender.py` from an earlier task was still sitting in the
  working directory and got imported instead of the newly updated file,
  since Python resolves local modules from the current working directory
  first. The scores looked "off" (genre worth only +1.0 instead of +2.0) —
  this was only caught by manually inspecting the printed "reasons" output
  against the expected weights, not by trusting the numbers at face value.
  Lesson: always re-verify actual output against expected math rather than
  assuming a rerun reflects the latest code.
- Confirmed backward compatibility by rerunning the existing "High-Energy
  Pop" / "Chill Lofi" / "Deep Intense Rock" profiles from `main.py` — none
  of them reference the new fields, and their scores/rankings matched
  prior runs exactly, confirming the new components are additive and
  opt-in rather than breaking existing behavior.


## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**Prompts used:**

<!-- Paste the key prompts you gave the agent -->

**What did the agent generate or change?**

<!-- List the files edited, code generated, or commands run -->

**What did you verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
