# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This recommender suggests up to 5 songs from an 18-song catalog based on a user's taste profile. It is designed for classroom exploration of how content-based filtering works — not for real production use.

It takes four inputs from the user:
- A favorite genre (e.g., "pop", "lofi")
- A favorite mood (e.g., "happy", "chill")
- A target energy level (0.0 = very calm, 1.0 = very intense)
- Whether or not they prefer acoustic-sounding music

It assumes users can describe their preferences as these four values and returns ranked songs with reasons explaining each recommendation.

---

## 3. How the Model Works

The system acts like a judge that gives every song in the catalog a score from 0 to 8, then picks the ones with the highest scores.

For each song, it checks four things:

1. **Does the genre match?** If yes, the song gets 3 points — this is the most important factor.
2. **Does the mood match?** If yes, the song gets 2 more points.
3. **How close is the energy?** A song that perfectly matches the user's target energy gets 2 points. Songs further away get fewer. This rewards closeness, not just "louder is better."
4. **Does the acoustic vibe fit?** If the user wants acoustic music and the song sounds acoustic (or vice versa), it gets 1 bonus point.

After every song has a score, the system sorts them from highest to lowest and returns the top results along with the specific reasons each song scored the way it did.

---

## 4. Data

The catalog contains **18 songs** across 10 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, hip-hop, classical, country, electronic, metal, reggae, and folk.

The original starter dataset had 10 songs. Eight additional songs were added to cover more genres and moods.

Moods represented: happy, chill, intense, relaxed, focused, moody.

**Gaps:** The dataset reflects western popular music. No Latin, K-pop, Afrobeats, gospel, or classical sub-genres are included. Lofi has 3 songs (17% of the catalog), while metal has only 1 song (5%). This uneven distribution means the system naturally serves lofi fans better than metal fans.

---

## 5. Strengths

- **Clear genre + mood profiles work well.** The High-Energy Pop Fan profile returned Sunrise City at rank 1 with a score of 7.94/8.0 — exactly the right answer.
- **Every recommendation is explainable.** There is no mystery score. Each result shows exactly which factors contributed and how many points each earned.
- **Energy scoring is nuanced.** Songs are not just ranked by "highest energy wins." A song at 0.82 energy scores better than one at 0.95 for a user who wants 0.85, which feels more accurate to real listening behavior.
- **The acoustic bonus adds useful diversity.** The Chill Lofi Studier's results included Wildflower Trail (folk) because it was acoustic and chill — a reasonable cross-genre suggestion.

---

## 6. Limitations and Bias

- **Genre carries too much weight.** Genre is worth 3 points — 37.5% of the maximum score. This means a pop song with the wrong mood (Gym Hero, score 5.84) ranked higher than a perfect-mood, high-energy non-pop song. The system may push users deeper into their current genre even when better matches exist in other genres.

- **Unequal genre representation creates bias.** Three of 18 songs are lofi, so lofi fans consistently get great results (top score: 8.00/8.0). Metal fans have only 1 song in the catalog. If this were a real product, metal listeners would be underserved compared to lofi listeners, simply because of how the data was built.

- **Tempo, valence, and danceability are never scored.** These three features are loaded from the CSV but unused. Storm Runner (rock, 152 BPM) and Iron Curtain (metal, 168 BPM) score nearly identically for the rock profile even though they feel very different.

- **Conflicting preferences break the system.** The adversarial profile (ambient genre + intense mood + high energy) exposed a fundamental flaw: ambient songs in the catalog are all low-energy and chill. The top result was Spacewalk Thoughts with a score of only 4.76, and it scored points only for genre and acousticness — not for mood or energy. The system has no way to resolve the contradiction between what the genre implies and what the mood/energy values request.

---

## 7. Evaluation

Four profiles were tested:

**1. High-Energy Pop Fan** (genre: pop, mood: happy, energy: 0.85)
Sunrise City ranked first with 7.94 points. Gym Hero (pop but not happy) came second. Results matched intuition — the system correctly identified the best genre+mood combination first.

**2. Chill Lofi Studier** (genre: lofi, mood: chill, energy: 0.35, likes_acoustic: True)
Library Rain scored a perfect 8.0/8.0 — exact match on all four factors. The interesting result was Wildflower Trail (folk) appearing at rank 4 because it was chill and acoustic, even though it is not lofi. This felt like a reasonable suggestion and shows the acoustic bonus adding useful cross-genre diversity.

**3. Deep Intense Rock Head** (genre: rock, mood: intense, energy: 0.92)
Storm Runner scored 7.98/8.0 (rank 1), which was the only rock song matching all criteria. Positions 2–5 all came from non-rock genres (pop, electronic, metal, hip-hop) that matched mood and energy but not genre. This revealed how thin the rock section of the catalog is — a real user would get only one truly relevant result.

**4. Conflicting Prefs (Adversarial)** (genre: ambient, mood: intense, energy: 0.90)
No song in the catalog is both ambient and intense. The top result was Spacewalk Thoughts, which matched the genre but scored poorly on energy proximity (0.76 out of 2.0) since ambient songs are inherently low-energy. The system returned a "genre wins" result that a real user would find useless.

**Weight-shift experiment:** Halving genre weight (3.0 → 1.5) and doubling energy weight (2.0 → 4.0) for the pop profile moved Rooftop Lights (high mood match, moderate energy) to rank 2 and pushed Gym Hero to rank 3. Sunrise City stayed at rank 1 because it matched all four factors. The experiment confirmed that the rankings are sensitive to weight changes, but when a song matches on all factors, no rebalancing can displace it.

---

## 8. Future Work

- **Add tempo range matching.** Allow users to specify a BPM range (e.g., "I want something between 80–110 BPM") and score songs that fall inside the range.
- **Add valence to scoring.** Right now "happy pop" and "melancholy pop" score the same for a happy profile. Including valence would let the system distinguish these.
- **Expand the catalog to at least 5 songs per genre.** One metal song means metal fans always get a mixed-genre top 5. Balanced representation would improve fairness.
- **Support soft genre preferences.** Instead of "pop only gets points," allow partial credit for related genres (e.g., indie pop = 1.5 points for a pop user rather than 0).
- **Handle conflicting preferences gracefully.** Detect when genre and mood/energy are in conflict and warn the user or suggest adjusting their inputs.

---

## 9. Personal Reflection

Building this showed me that even a simple four-factor scoring rule produces surprisingly strong opinions. The genre weight felt obviously right when I wrote it, but testing adversarial profiles revealed that it can completely override what a user actually wants to feel. A person asking for "something intense" should not get a calm ambient song just because they listed ambient as their favorite genre — but that is exactly what happened.

It also made me realize how much data representation matters. Giving lofi three catalog slots versus metal one is not neutral — it is a design choice that quietly advantages some users over others. Real systems like Spotify face this problem at enormous scale, where catalog gaps in underrepresented genres affect millions of listeners who never see an explanation for why their recommendations feel off. Being able to print "this ranked first because genre match (+3.0), energy proximity (+1.94)" made every bug and bias immediately visible, which made me appreciate explainability as a core design requirement, not a nice-to-have feature.

---
