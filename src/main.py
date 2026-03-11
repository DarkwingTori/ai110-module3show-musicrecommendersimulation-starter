"""
Command line runner for the Music Recommender Simulation.

Runs four user profiles through the recommender and prints ranked results,
then runs a weight-shift experiment to test scoring sensitivity.
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Four test profiles: 3 standard + 1 adversarial
    profiles = [
        {
            "name": "High-Energy Pop Fan",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "likes_acoustic": False,
        },
        {
            "name": "Chill Lofi Studier",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
        },
        {
            "name": "Deep Intense Rock Head",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "likes_acoustic": False,
        },
        {
            "name": "Conflicting Prefs (Adversarial)",
            "genre": "ambient",
            "mood": "intense",
            "energy": 0.90,
            "likes_acoustic": True,
        },
    ]

    for profile in profiles:
        name = profile.pop("name")
        print(f"\n{'='*50}")
        print(f"Profile: {name}")
        print(f"{'='*50}\n")
        recommendations = recommend_songs(profile, songs, k=5)
        for song, score, reasons in recommendations:
            print(f"  {song['title']} by {song['artist']}  —  Score: {score:.2f}")
            for reason in reasons:
                print(f"    • {reason}")
            print()
        profile["name"] = name  # restore for clarity

    # --- EXPERIMENT: Halve genre weight (3.0 → 1.5), double energy weight (2.0 → 4.0) ---
    # Testing whether energy-first scoring changes results for the pop profile.
    print(f"\n{'='*50}")
    print("EXPERIMENT: genre x1.5, energy x4.0  (pop/happy profile)")
    print(f"{'='*50}\n")
    exp_prefs = {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False}
    exp_scored = []
    for song in songs:
        score = 0.0
        reasons = []
        if song.get("genre") == exp_prefs["genre"]:
            score += 1.5   # was 3.0
            reasons.append("genre match (+1.5)")
        if song.get("mood") == exp_prefs["mood"]:
            score += 2.0
            reasons.append("mood match (+2.0)")
        energy_pts = 4.0 * (1 - abs(song.get("energy", 0.0) - exp_prefs["energy"]))  # was 2.0x
        score += energy_pts
        reasons.append(f"energy proximity (+{energy_pts:.2f})")
        if not exp_prefs["likes_acoustic"] and song.get("acousticness", 0.0) < 0.4:
            score += 1.0
            reasons.append("non-acoustic match (+1.0)")
        exp_scored.append((song, score, reasons))
    exp_scored.sort(key=lambda x: x[1], reverse=True)
    print("Top 3 with experimental weights:\n")
    for song, score, reasons in exp_scored[:3]:
        print(f"  {song['title']} by {song['artist']}  —  Score: {score:.2f}")
        for r in reasons:
            print(f"    • {r}")
        print()


if __name__ == "__main__":
    main()
