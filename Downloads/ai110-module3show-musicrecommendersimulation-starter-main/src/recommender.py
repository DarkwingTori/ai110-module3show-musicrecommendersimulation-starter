import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_song_dict(song: Dict, user: Dict) -> Tuple[float, str]:
    """
    Score a single song (as a dict) against a user preferences dict.
    Returns (score, explanation).

    Scoring recipe:
      +2.0  genre match
      +1.0  mood match
      0–1.5 energy proximity: 1.5 × (1 − |song.energy − user.target_energy|)
      +0.5  acoustic bonus if user.likes_acoustic and song.acousticness > 0.6
    Max possible score: 5.0
    """
    score = 0.0
    reasons = []

    if song.get("genre") == user.get("genre"):
        score += 2.0
        reasons.append("Genre match (+2.0)")

    if song.get("mood") == user.get("mood"):
        score += 1.0
        reasons.append("Mood match (+1.0)")

    energy_diff = abs(float(song.get("energy", 0)) - float(user.get("target_energy", 0.5)))
    energy_pts = round(1.5 * (1 - energy_diff), 2)
    score += energy_pts
    reasons.append(f"Energy proximity (+{energy_pts})")

    if user.get("likes_acoustic") and float(song.get("acousticness", 0)) > 0.6:
        score += 0.5
        reasons.append("Acoustic bonus (+0.5)")

    return round(score, 2), ", ".join(reasons)


def _score_song_obj(song: Song, user: UserProfile) -> Tuple[float, str]:
    """
    Score a single Song dataclass object against a UserProfile.
    Returns (score, explanation).
    """
    score = 0.0
    reasons = []

    if song.genre == user.favorite_genre:
        score += 2.0
        reasons.append("Genre match (+2.0)")

    if song.mood == user.favorite_mood:
        score += 1.0
        reasons.append("Mood match (+1.0)")

    energy_diff = abs(song.energy - user.target_energy)
    energy_pts = round(1.5 * (1 - energy_diff), 2)
    score += energy_pts
    reasons.append(f"Energy proximity (+{energy_pts})")

    if user.likes_acoustic and song.acousticness > 0.6:
        score += 0.5
        reasons.append("Acoustic bonus (+0.5)")

    return round(score, 2), ", ".join(reasons)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, _score_song_obj(song, user)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, explanation = _score_song_obj(song, user)
        return explanation


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
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
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Returns list of (song_dict, score, explanation) sorted by score descending.
    """
    scored = []
    for song in songs:
        score, explanation = _score_song_dict(song, user_prefs)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
