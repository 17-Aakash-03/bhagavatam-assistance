"""Verse lookup. For a small verse collection we simply keep everything in
memory. Later, when you have thousands of verses, replace pick_verses()
with an embedding / vector search (for example ChromaDB)."""

import json
import random
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "verses.json"

with open(DATA_FILE, encoding="utf-8") as f:
    VERSES = json.load(f)

BY_ID = {v["id"]: v for v in VERSES}

THEME_KEYWORDS = {
    "depression": ["depress", "sad", "hopeless", "lonely", "alone", "cry", "empty",
                   "worthless", "grief", "hurt", "low mood", "udaas", "dukhi"],
    "anxiety": ["anxi", "fear", "afraid", "worry", "worried", "stress", "panic",
                "nervous", "tension", "overthink", "dar lag"],
    "motivation": ["motiv", "purpose", "meaning", "lazy", "goal", "direction",
                   "career", "procrastinat", "give up", "aim"],
    "peace": ["peace", "angry", "anger", "restless", "desire", "craving",
              "expect", "calm", "jealous", "attachment"],
    "practice": ["meditat", "pray", "practice", "devotion", "chant", "japa"],
}


def detect_theme(text: str) -> str:
    lowered = text.lower()
    scores = {t: sum(lowered.count(k) for k in kws) for t, kws in THEME_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "peace"


def pick_verses(theme: str, k: int = 2):
    matches = [v for v in VERSES if theme in v["themes"]]
    return random.sample(matches, min(k, len(matches)))


def verse_card(v: dict) -> dict:
    """Only the fields the browser needs."""
    return {
        "id": v["id"],
        "ref": v["ref"],
        "meaning": v["meaning"],
        "url": v["url"],
        "sanskrit": v.get("sanskrit", ""),
        "translit": v.get("translit", ""),
    }


def catalog_text() -> str:
    return "\n".join(
        f"{v['id']} | {v['ref']} | {', '.join(v['themes'])} | {v['meaning']}"
        for v in VERSES
    )