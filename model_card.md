# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The system over-prioritizes genre-labeled songs from the most common genre (lofi, 30% of the catalog) because genre carries double the point weight of mood, so users who define their taste primarily by feel rather than genre label get systematically under-scored even when a good mood/energy match exists. This creates a filter bubble where lofi-genre users keep getting confidently ranked results while mood-driven users get thinner, less certain lists. Separately, because no song in the dataset has an energy value below 0.28 or above 0.93, users targeting the true extremes of the energy scale are structurally unable to score well no matter how the weights are tuned — the closeness math is fair, but the data simply can't serve them, which the scoring rule has no way to detect or flag.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
