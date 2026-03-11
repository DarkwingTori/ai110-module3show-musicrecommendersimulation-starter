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

**Non-Intended Use:** This system should not be used to make real music recommendations for actual users. It has no access to streaming data, cannot learn from listening history, and only has 18 songs in its catalog. It should not be used to rank or judge musical quality, claim that one song is objectively "better" than another, or make any decisions that affect real people's listening experience or career.

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

**Biggest learning moment:** The adversarial profile test was the clearest turning point. I built the scoring logic thinking genre should matter most, and it made sense in isolation. Then a profile with genre: "ambient", mood: "intense", energy: 0.90 completely broke the system — the top result was a calm, quiet ambient song that matched the genre but ignored everything else the user asked for. That moment showed me that weights are assumptions, and assumptions only reveal themselves when you push against them with edge cases.

**How AI tools helped — and when I needed to double-check:** AI tools were useful for generating the initial scoring logic structure, expanding the song catalog with diverse genres, and suggesting how to format the CLI output. But I had to verify the math manually every time. When I asked for "reward closeness in energy," the suggested formula was right, but I traced through it with actual numbers (|0.82 - 0.80| = 0.02, so 2.0 × 0.98 = 1.96) before trusting it. AI tools are fast at producing plausible code, but they do not tell you whether the logic is actually doing what you want — that requires running it and reading the output critically.

**What surprised me about simple algorithms:** I expected a four-rule scoring system to feel robotic and obvious. What surprised me was how often the results matched musical intuition — Library Rain scoring 8.0/8.0 for the lofi studier profile, or Wildflower Trail appearing in that same list because it was acoustic and chill even though it is folk. A few numerical thresholds, applied consistently, produce something that genuinely feels like a recommendation. The surprise is not that it works — it is that it works for reasons you can read and explain, which most real systems cannot do.

**What I would try next:** I would add valence to the scoring so the system could distinguish between "happy pop" and "sad pop." I would also experiment with allowing users to set two genres with different weights instead of one, and I would try building a simple diversity penalty so the top 5 results cannot all come from the same genre even if they score highest.

---
