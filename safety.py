"""If the user mentions self-harm, skip the normal flow and show helpline info."""

CRISIS_PATTERNS = [
    "suicide", "suicidal", "kill myself", "killing myself", "end my life",
    "end it all", "want to die", "wanna die", "don't want to live",
    "dont want to live", "do not want to live", "no reason to live",
    "better off dead", "hurt myself", "harm myself", "self harm",
    "self-harm", "cut myself", "take my own life",
    # Hindi / Hinglish
    "khudkushi", "aatmahatya", "marna chahta", "marna chahti",
    "mar jana chahta", "mar jana chahti", "jeena nahi chahta",
    "jeena nahi chahti", "jine ka mann nahi", "khud ko khatam",
    "आत्महत्या", "मरना चाहता", "मरना चाहती", "जीना नहीं चाहता",
    "जीना नहीं चाहती",
]

CRISIS_MESSAGE = (
    "I'm really glad you told me, and I'm sorry you are in so much pain. "
    "Your life matters, and you do not have to carry this alone.\n\n"
    "Please reach out to someone who can help right now:\n"
    "• Tele-MANAS (India, free, 24x7): 14416 or 1800-891-4416\n"
    "• If you are in immediate danger, call 112 (India's emergency number) "
    "or go to the nearest hospital.\n"
    "• Please tell a family member or a friend near you, and try not to be alone tonight.\n\n"
    "I am not a replacement for a counsellor or a doctor, but I am here to keep talking with you."
)


def is_crisis(text: str) -> bool:
    lowered = text.lower().replace("’", "'")
    return any(pattern in lowered for pattern in CRISIS_PATTERNS)