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

# who is speaking and why (shown under each verse)
CONTEXT = {
    "sb-1-2-6": "Suta Gosvami answers the sages of Naimisharanya who asked what the highest duty of life is.",
    "sb-1-2-8": "Suta Gosvami explains why duties are only tiring labor without love for the Lord's message.",
    "sb-1-2-17": "Suta Gosvami explains how hearing about the Lord purifies the heart.",
    "sb-1-2-18": "Suta Gosvami explains how regular hearing of the Bhagavatam makes faith steady.",
    "sb-1-8-25": "Queen Kunti prays to Krishna after the great war, remembering that in her hardest days she felt closest to Him. This is her personal prayer, not advice to seek suffering.",
    "sb-1-8-26": "Queen Kunti continues her prayer, saying humility opens the heart to the Lord.",
    "sb-2-3-17": "Sukadeva Gosvami tells King Parikshit how precious each day of life is.",
    "sb-3-25-25": "Lord Kapila teaches his mother Devahuti the value of good company.",
    "sb-7-5-23": "Prahlada Maharaja lists nine simple ways to practice devotion.",
    "sb-7-6-1": "Prahlada Maharaja teaches his young classmates not to postpone what matters most.",
    "sb-10-14-8": "Brahma prays to Krishna, speaking of accepting life's difficulties patiently.",
    "sb-10-14-58": "Brahma's prayer to Krishna, describing the peace of those who take shelter of Him.",
    "sb-11-2-37": "Sage Kavi explains to King Nimi where fear comes from and how it ends.",
    "sb-11-8-44": "The story of Pingala, told to King Yadu, about the peace found by letting go of expectations.",
    "sb-11-23-42": "From the song of a suffering brahmana, retold by Krishna to Uddhava, about the mind as the cause of joy and distress.",
    "sb-12-3-51": "Sukadeva Gosvami tells Parikshit the one great quality of the present age.",
    "sb-12-3-52": "Sukadeva Gosvami continues: chanting gives what earlier ages reached by other practices.",
}
for _v in VERSES:
    _v["context"] = CONTEXT.get(_v["id"], "")

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
        "context": v.get("context", ""),
    }


def catalog_text() -> str:
    return "\n".join(
        f"{v['id']} | {v['ref']} | {', '.join(v['themes'])} | {v['meaning']}"
        for v in VERSES
    )