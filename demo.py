"""Demo mode: used online, where the local AI model is not available. Replies are scripted."""

from rag import detect_theme, pick_verses, verse_card

QUESTIONS = [
    "I'm sorry you are going through this. Can you tell me what happened, or what has been making you feel this way?",
    "Thank you for sharing that. How long have you been feeling like this, and have you told anyone close to you about it?",
    "I hear you. How are your sleep, food and daily routine these days?",
]

# a direct first sentence for when the person asks a question such as "What is motivation?"
DIRECT = {
    "depression": "Sadness or depression is a heavy, lasting low mood that makes everything feel pointless or tiring. It is not weakness, and it can improve with support.",
    "anxiety": "Anxiety is a constant feeling of worry or fear, even when nothing is wrong right now. It is very common, and it can be calmed step by step.",
    "motivation": "Motivation is the inner drive that helps us start something and keep going toward a goal.",
    "peace": "Peace of mind is a calm, steady state in which worries, anger and cravings no longer pull us in every direction.",
    "practice": "Spiritual practice means a simple daily habit, such as chanting, prayer, or hearing sacred stories, that steadies the heart.",
}

ANSWERS = {
    "depression": {
        "image": "sunrise",
        "message": "Thank you for trusting me with all this. Feeling low and heavy is painful, and it does not make you weak. The Bhagavatam teaches that the ups and downs of life are temporary, and that the heart finds comfort through patience, good company and prayer.",
        "steps": [
            "Take a 10-minute walk outside in daylight.",
            "Eat something warm and try to sleep at a fixed time.",
            "Message or call one person you trust and tell them how you feel.",
            "Sit quietly for 5 minutes and pray or chant in whatever way feels natural.",
            "If this feeling stays for more than two weeks, please talk to a doctor or counsellor. Asking for help is a strength.",
        ],
    },
    "anxiety": {
        "image": "river",
        "message": "Worry can feel like a storm that never stops. The Bhagavatam says fear grows when we forget who we really are, and that steady faith and a calm routine bring the mind back to shore.",
        "steps": [
            "Breathe in for 4 counts and out for 6 counts, five times.",
            "Write down what worries you, then circle only what you can act on today.",
            "Reduce screen time and caffeine in the evening.",
            "Chant or pray quietly for a few minutes.",
            "If anxiety is affecting your daily life, please speak to a doctor or counsellor.",
        ],
    },
    "motivation": {
        "image": "mountain",
        "message": "Each day is precious, and the Bhagavatam reminds us that purpose grows from small, steady steps rather than from big bursts of energy.",
        "steps": [
            "Choose one tiny task for today and finish it.",
            "Wake up and sleep at a fixed time for the next week.",
            "Spend 10 minutes in the morning in quiet reading or prayer.",
            "Write down what you want your life to stand for.",
            "Share your goal with a friend who will encourage you.",
        ],
    },
    "peace": {
        "image": "lotus",
        "message": "The Bhagavatam points to letting go of constant expectations and to simple, regular spiritual practice as sources of lasting peace.",
        "steps": [
            "Spend 5 minutes in silence every morning.",
            "Notice one expectation you are holding and consciously loosen it.",
            "Be kind in one small way to someone today.",
            "Chant or pray in the evening before sleeping.",
            "Keep a short gratitude note of three things each night.",
        ],
    },
    "practice": {
        "image": "lamp",
        "message": "The Bhagavatam describes many easy ways to begin, and you can choose the ones that feel natural.",
        "steps": [
            "Pick a fixed time and place for your practice.",
            "Start with just 5 minutes of chanting or silent prayer.",
            "Read or listen to one short passage each day.",
            "Light a lamp or incense as a gentle signal to your mind.",
            "Increase the time slowly instead of forcing yourself.",
        ],
    },
}


def demo_reply(user_texts, info_only=False, all_text=""):
    n = len(user_texts)

    # a direct question ("What is motivation?") is answered at once, like the real model does
    if info_only:
        theme = detect_theme(all_text or " ".join(user_texts))
        info = ANSWERS[theme]
        return {
            "mode": "answer",
            "message": DIRECT[theme] + " " + info["message"],
            "steps": info["steps"],
            "verses": [verse_card(v) for v in pick_verses(theme, 2)],
            "image_theme": info["image"],
        }

    # a personal feeling: ask gentle questions first
    if n < 4:
        return {
            "mode": "ask",
            "message": QUESTIONS[min(max(n - 1, 0), len(QUESTIONS) - 1)],
            "steps": [],
            "verses": [],
            "image_theme": "lotus",
        }

    theme = detect_theme(" ".join(user_texts))
    info = ANSWERS[theme]
    return {
        "mode": "answer",
        "message": info["message"],
        "steps": info["steps"],
        "verses": [verse_card(v) for v in pick_verses(theme, 2)],
        "image_theme": info["image"],
    }