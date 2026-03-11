import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes. Required by tests/test_recommender.py"""
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
    """Represents a user's taste preferences. Required by tests/test_recommender.py"""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score all songs against the user profile and return the top k sorted by score."""
        scored = []
        for song in self.songs:
            score = 0.0
            if song.genre == user.favorite_genre:
                score += 3.0
            if song.mood == user.favorite_mood:
                score += 2.0
            score += 2.0 * (1 - abs(song.energy - user.target_energy))
            if user.likes_acoustic and song.acousticness > 0.6:
                score += 1.0
            elif not user.likes_acoustic and song.acousticness < 0.4:
                score += 1.0
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-English explanation of why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre '{song.genre}' matches your favorite")
        else:
            reasons.append(f"genre '{song.genre}' differs from your favorite '{user.favorite_genre}'")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood '{song.mood}' matches your preference")
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.1:
            reasons.append("energy level is very close to your target")
        elif energy_diff < 0.3:
            reasons.append("energy level is somewhat close to your target")
        else:
            reasons.append("energy level differs from your target")
        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append("has the acoustic sound you enjoy")
        elif not user.likes_acoustic and song.acousticness < 0.4:
            reasons.append("has the non-acoustic style you prefer")
        return "Recommended because: " + "; ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting numeric fields to float or int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; return (score, reasons)."""
    score = 0.0
    reasons = []

    if song.get("genre") == user_prefs.get("genre"):
        score += 3.0
        reasons.append("genre match (+3.0)")

    if song.get("mood") == user_prefs.get("mood"):
        score += 2.0
        reasons.append("mood match (+2.0)")

    energy_pts = 2.0 * (1 - abs(song.get("energy", 0.0) - user_prefs.get("energy", 0.5)))
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic and song.get("acousticness", 0.0) > 0.6:
        score += 1.0
        reasons.append("acousticness match (+1.0)")
    elif not likes_acoustic and song.get("acousticness", 0.0) < 0.4:
        score += 1.0
        reasons.append("non-acoustic match (+1.0)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score all songs, sort by score descending, return top k as (song, score, reasons)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
