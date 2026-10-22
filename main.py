import json
import os
import re
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

from flask import Flask, jsonify, request, send_from_directory

from demo import demo_reply
from hinglish_answer import hinglish_answer
from prompts import build_system_prompt
from rag import BY_ID, VERSES, detect_theme, pick_verses, verse_card
from safety import CRISIS_MESSAGE, is_crisis

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()      # ollama | claude | demo
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
IMAGE_THEMES = {"sunrise", "lotus", "river", "mountain", "lamp"}
THEME_IMAGE = {"depression": "sunrise", "anxiety": "river", "motivation": "mountain",
               "peace": "lotus", "practice": "lamp"}

app = Flask(__name__, static_folder="static", static_url_path="/static")

# which picture topic fits the question (first topic whose words appear wins)
SCENE_TOPICS = [
    ("loss", ["death", "died", "lost my dad", "lost my mom", "lost my father", "lost my mother", "lost my friend", "lost someone", "passed away", "grief", "funeral", "miss him", "miss her", "guzar", "nidhan", "mrityu"]),
    ("study", ["exam", "marks", " study", "studies", "college", "school", "result", "student", "homework", "teacher",
               "padhai", "padh ", "board", "neet", "jee"]),
    ("work", ["job", "office", "boss", "career", "salary", "interview", "business", "naukri", "kaam", "colleague"]),
    ("family", ["family", "mother", "father", "parents", " mom ", " dad ", "brother", "sister", "wife", "husband",
                "mummy", "papa", "ghar", "bhai", "behen"]),
    ("friends", ["friend", "relationship", "breakup", "girlfriend", "boyfriend", "partner", "lonely", "alone",
                 "dost", "pyaar", "pyar", "akela", "rishta"]),
    ("sleep", ["sleep", "insomnia", "tired", "neend", " rest "]),
    ("anger", [" angry", " anger", "gussa", "irritat", "jealous"]),
    ("anxiety", ["anxi", "fear", "panic", "worry", "worried", "stress", "tension", "nervous", "ghabra", "chinta", "darr"]),
    ("depression", ["depress", " sad", "hopeless", " cry", "empty", "worthless", "udaas", "udasi", "dukhi"]),
    ("motivation", ["motiv", "purpose", "goal", "lazy", "direction", "give up", "procrastinat", "success"]),
    ("practice", ["pray", "chant", "devotion", "temple", "japa", "krishna", " god ", "bhagavatam", "bhakti", "meditat"]),
    ("peace", ["peace", " calm", " mind", "restless", "desire", "craving"]),
]

SENSITIVE_WORDS = ["sex", "porn", "nude", "masturbat", "erotic", "orgasm", "intercourse"]

SENSITIVE_REPLY_EN = (
    "I am a spiritual guidance app, so I am not the right place to explain this topic. For questions about sex "
    "or sexual health, a doctor, a counsellor or a trusted elder can help you properly. If desire, guilt or a "
    "restless mind is troubling you, please tell me how you are feeling and I will listen."
)
SENSITIVE_REPLY_HI = (
    "Main ek adhyatmik margdarshan app hoon, isliye is vishay ko samjhane ki sahi jagah nahi hoon. Is tarah ke "
    "sawaalon ke liye doctor, counsellor ya kisi bharose ke bade se baat kijiye. Agar ichha, glani ya bechain mann "
    "aapko pareshan kar raha hai, to mujhe bataiye ki aap kaisa mehsoos kar rahe hain."
)


def is_sensitive(text: str) -> bool:
    words = re.findall(r"[a-z]+", text.lower())
    return any(w.startswith(tuple(SENSITIVE_WORDS)) for w in words)


# topics this app is not made for (it is a spiritual guidance app)
OFFTOPIC_WORDS = [
    "python", "java ", "javascript", "c++", " code", "coding", "programming", "software", "website",
    " ai ", "ai-ml", "ai/ml", " ml ", "machine learning", "deep learning", "data science", "project idea",
    "project ideas", "projects for", "recipe", "movie", "cricket", "ipl", "stock market", "bitcoin", "crypto",
    "weather", "translate", "equation", "algebra", "calculus", "essay", "resume", "laptop", "football",
]
EMOTION_WORDS = [
    "feel", "sad", "depress", "anxi", "stress", "scared", "afraid", "fear", "worried", "worry", "lonely", "alone",
    "angry", "anger", "tired", "overwhelm", "hopeless", "pressure", "cry", "upset", "hurt", "tension", "panic",
    "udaas", "dukhi", "ghabra", "chinta", "darr", "akela", "gussa", "thak",
]

OFFTOPIC_REPLY_EN = (
    "I am a spiritual guidance app, so I am not the best place for this kind of request. A general AI assistant "
    "or your teacher will help you better here. But if the work, study or stress around it is weighing on you, "
    "tell me how you feel and I will listen."
)
OFFTOPIC_REPLY_HI = (
    "Main ek adhyatmik margdarshan app hoon, isliye is tarah ke sawaal ke liye sahi jagah nahi hoon. Iske liye "
    "koi general AI assistant ya aapke teacher behtar madad karenge. Lekin agar is kaam ya padhai ka tanav aapko "
    "bhaari lag raha hai, to mujhe bataiye ki aap kaisa mehsoos kar rahe hain."
)

SMALL_TALK_WORDS = {"thanks", "thank", "thankyou", "ty", "dhanyavad", "shukriya", "bye", "goodbye",
                    "hi", "hello", "hey", "namaste", "namaskar", "pranam", "you", "ok", "okay"}
SMALL_TALK_REPLY = (
    "Namaste \U0001F64F I am here whenever you want to talk. Tell me what is on your heart, or ask me anything."
)


def is_offtopic(text: str) -> bool:
    lowered = " " + text.lower() + " "
    if any(w in lowered for w in EMOTION_WORDS):
        return False
    if " project" in lowered and is_info_question(text):
        return True
    return any(w in lowered for w in OFFTOPIC_WORDS)


def is_small_talk(text: str) -> bool:
    tokens = re.findall(r"[a-z]+", text.lower())
    return 0 < len(tokens) <= 4 and all(t in SMALL_TALK_WORDS for t in tokens)


def scene_topic(text: str, info_only: bool = False):
    lowered = " " + text.lower() + " "
    for topic, words in SCENE_TOPICS:
        if any(w in lowered for w in words):
            return topic
    return "knowledge" if info_only else None


# ---------------------------------------------------------------- helpers

def has_api_key() -> bool:
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    return bool(key) and key != "your-key-here"


def parse_json(text: str):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None


def is_info_question(text: str) -> bool:
    """True for a question or a request for information (not a personal feeling)."""
    t = text.strip().lower().lstrip("\"'\u201c\u201d\u2018\u2019 ")
    starts = ("what", "why", "how", "who", "when", "where", "which", "explain", "tell me", "define",
              "meaning of", "suggest", "give me", "give some", "list", "recommend", "show me",
              "kya ", "kaise", "kyun", "kyon", "kaun", "kab ", "kitna", "batao", "bataiye", "samjhao")
    return "?" in t or t.startswith(starts)


HINGLISH_WORDS = {
    "mujhe", "mera", "meri", "mere", "hai", "hain", "hoon", "nahi", "nahin", "kya", "bahut",
    "rahi", "raha", "rahe", "aap", "aapko", "kuch", "kyun", "kyon", "kaise", "udaas", "udasi",
    "dukhi", "thak", "thaka", "neend", "khana", "ghabrahat", "chinta", "tanav", "gussa",
    "akela", "akelapan", "dost", "ghar", "padhai", "kaam", "zindagi", "hota", "hoti",
    "lagta", "lagti", "karna", "karta", "karti", "bohot", "thoda", "bahot", "sab", "koi",
    "mann", "dil",
}

HINGLISH_ASKS = [
    "Yeh sunkar mujhe bura laga. Kya aap bata sakte hain ki kya hua, ya kis wajah se aisa mehsoos ho raha hai?",
    "Samajh sakta hoon, yeh bhaari hota hai. Yeh kab se ho raha hai, aur kya aapne kisi apne ko bataya hai?",
    "Batane ke liye shukriya. Aapki neend, khana aur roz ka routine abhi kaisa chal raha hai?",
]


def looks_hinglish(text: str) -> bool:
    words = re.findall(r"[a-z]+", text.lower())
    return any(w in HINGLISH_WORDS for w in words)


def hinglish_chat(user_texts) -> bool:
    """True when at least half of the user's messages look like Hinglish."""
    hits = sum(1 for t in user_texts if looks_hinglish(t))
    return hits > 0 and hits * 2 >= len(user_texts)


# ---------------------------------------------------------------- Ollama (free, local)

ASK_TOPICS = [
    "what happened, or what is making them feel this way",
    "how long they have felt like this, and whether they have told anyone close to them",
    "how their sleep, food and daily routine are these days",
]

OLLAMA_RULES = """You are "Bhagavatam Assistance", a warm, calm and respectful guide who offers spiritual comfort inspired by the Srimad-Bhagavatam.
You are NOT a doctor or therapist. Never diagnose and never give medical advice.
Reply in the same language as the user's latest message (English, Hindi or Hinglish).
Be kind and simple. Never blame the person. Never mention verse numbers or quote verses; the app shows verses separately.
IMPORTANT: Only say "the Bhagavatam teaches/says/reminds" about ideas from this list, and never invent stories, images or metaphors about the Bhagavatam:
- human life is short and every day is precious, so time spent on what uplifts the heart is not wasted;
- fear comes from forgetting our true identity and mistaking the temporary body for the self;
- craving material pleasures causes deep unhappiness, and letting go of that craving brings peace;
- hearing and chanting about the Lord, and the company of good devotees, purify and nourish the heart;
- chanting the holy names can free a person from attachment;
- a wise person begins spiritual practice early, and even sincere small practice is valuable;
- difficulties can be accepted patiently while staying humble and prayerful.
For everything else give plain, kind, practical advice in your own voice, without attributing it to the Bhagavatam.
If the person asks a question (for example "What is motivation?"), answer that question directly in the first sentence.
Reply with ONLY one JSON object and nothing else."""


def ollama_system_prompt(mode: str, user_turns: int) -> str:
    if mode == "ask":
        topic = ASK_TOPICS[min(user_turns - 1, len(ASK_TOPICS) - 1)]
        return (OLLAMA_RULES + "\n\nTASK: The person shared something personal. Write 1 short sentence of "
                "empathy, then ask exactly ONE gentle question about: " + topic +
                ". Do not give advice yet.\n"
                'Format: {"message": "your empathy sentence and your question"}')
    return (OLLAMA_RULES + "\n\nTASK: Give the full answer. Write 2 to 4 caring sentences that reflect what "
            "the person told you. If it fits, include ONE gentle idea from the allowed list above (for "
            "example: time is precious, good company, prayer or chanting, letting go of craving). "
            "Then give 4 or 5 small practical steps they can do today (short walk, "
            "regular sleep and meals, talking to a trusted person, a few quiet minutes of prayer or "
            "chanting, writing thoughts down). If the problem is heavy or long-lasting, one step must "
            "encourage talking to a doctor or counsellor.\n"
            'Format: {"message": "your caring sentences", "steps": ["step 1", "step 2", "step 3", "step 4"]}')


def call_ollama(history, mode, user_turns, regen=False):
    body = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "system", "content": ollama_system_prompt(mode, user_turns)}] + history,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.9 if regen else 0.4},
    }
    req = urllib.request.Request(
        OLLAMA_URL + "/api/chat",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        out = json.loads(resp.read().decode("utf-8"))
    text = out.get("message", {}).get("content", "")
    data = parse_json(text)
    if data is None:
        data = {"message": text.strip()}
    return data


def build_ollama_result(data, mode, all_text, info_only=False):
    message = str(data.get("message", "")).strip() or "Could you tell me a little more about how you feel?"
    if mode == "ask":
        return {"mode": "ask", "message": message, "steps": [], "verses": [], "image_theme": None}
    steps = []
    raw = data.get("steps")
    if isinstance(raw, list):
        steps = [re.sub(r"^\s*\d+[.)]\s*", "", str(s)).strip() for s in raw if str(s).strip()][:6]
        steps = [(s[0].upper() + s[1:]) + ("" if s.endswith((".", "!", "?")) else ".") for s in steps if s]
    theme = detect_theme(all_text)
    return {
        "mode": "answer",
        "message": message,
        "steps": steps,
        "verses": [verse_card(v) for v in pick_verses(theme, 2)],   # chosen by code, never invented
        "image_theme": scene_topic(all_text, info_only) or THEME_IMAGE.get(theme, "lotus"),
    }


# ---------------------------------------------------------------- Claude (paid, optional)

def call_claude(history, user_turns):
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=CLAUDE_MODEL, max_tokens=1500,
        system=build_system_prompt(user_turns), messages=history,
    )
    text = "".join(b.text for b in response.content if getattr(b, "type", "") == "text")
    data = parse_json(text)
    if data is None:
        data = {"mode": "ask", "message": text.strip(), "steps": [], "verse_ids": []}
    return data


def normalize_claude(data, all_user_text):
    mode = data.get("mode") if data.get("mode") in ("ask", "answer") else "ask"
    message = str(data.get("message", "")).strip() or "Could you tell me a little more?"
    steps, verses = [], []
    if mode == "answer":
        raw_steps = data.get("steps")
        if isinstance(raw_steps, list):
            steps = [str(s) for s in raw_steps if str(s).strip()][:6]
        raw_ids = data.get("verse_ids")
        ids = []
        for i in raw_ids if isinstance(raw_ids, list) else []:
            if i in BY_ID and i not in ids:
                ids.append(i)
        verses = [verse_card(BY_ID[i]) for i in ids[:3]]
        if not verses:
            verses = [verse_card(v) for v in pick_verses(detect_theme(all_user_text), 2)]
    image = data.get("image_theme")
    return {"mode": mode, "message": message, "steps": steps, "verses": verses,
            "image_theme": image if image in IMAGE_THEMES else "lotus"}


# ---------------------------------------------------------------- routes

NOTICE_TEXTS = {SENSITIVE_REPLY_EN, SENSITIVE_REPLY_HI, OFFTOPIC_REPLY_EN, OFFTOPIC_REPLY_HI, SMALL_TALK_REPLY}


def drop_notice_turns(items):
    """Forget messages that only got a short notice (off-topic, small talk, ...) and those notices."""
    out = []
    for it in items:
        if it["role"] == "user":
            t = it["content"]
            if is_sensitive(t) or is_small_talk(t) or is_offtopic(t):
                continue
        elif it["mode"] == "notice" or it["content"] in NOTICE_TEXTS:
            continue
        out.append(it)
    while out and out[0]["role"] != "user":
        out.pop(0)
    return out


def finished_answer(it) -> bool:
    """True if this assistant message was a full answer (the browser may not say; a question ends with ?)."""
    if it["role"] != "assistant":
        return False
    if it["mode"]:
        return it["mode"] == "answer"
    return not it["content"].rstrip().endswith("?")


def notice(message):
    """A short reply that is not part of the conversation (the browser does not remember it)."""
    return jsonify({"mode": "notice", "message": message, "steps": [], "verses": [],
                    "image_theme": None, "demo": False})


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    raw = payload.get("messages")
    items = []
    for m in raw if isinstance(raw, list) else []:
        if not isinstance(m, dict):
            continue
        role, content = m.get("role"), str(m.get("content", "")).strip()
        if role in ("user", "assistant") and content:
            items.append({"role": role, "content": content, "mode": str(m.get("mode", ""))})
    items = items[-20:]
    while items and items[0]["role"] != "user":
        items.pop(0)
    if not items or items[-1]["role"] != "user":
        return jsonify({"mode": "error", "message": "Please type a message first.",
                        "steps": [], "verses": []})

    last = items[-1]["content"]

    if is_crisis(last):
        return jsonify({"mode": "crisis", "message": CRISIS_MESSAGE, "steps": [], "verses": [],
                        "image_theme": None, "demo": False})

    hinglish_last = looks_hinglish(last)
    if is_sensitive(last):
        return notice(SENSITIVE_REPLY_HI if hinglish_last else SENSITIVE_REPLY_EN)
    if is_small_talk(last):
        return notice(SMALL_TALK_REPLY)
    if is_offtopic(last):
        return notice(OFFTOPIC_REPLY_HI if hinglish_last else OFFTOPIC_REPLY_EN)

    # an "episode" is the conversation since the last finished answer, so a new question
    # is not mixed into an earlier feeling-chat
    items = drop_notice_turns(items)
    start = 0
    for i, it in enumerate(items):
        if finished_answer(it):
            start = i + 1
    episode = items[start:]
    while episode and episode[0]["role"] != "user":
        episode.pop(0)
    episode = [{"role": it["role"], "content": it["content"]} for it in episode]
    user_texts = [m["content"] for m in episode if m["role"] == "user"]
    n = len(user_texts)

    info_only = is_info_question(last)          # a direct question is answered at once
    if info_only:
        # keep a little context so follow-ups like "give me an example" make sense
        history = [{"role": it["role"], "content": it["content"]} for it in items[-6:]]
        while history and history[0]["role"] != "user":
            history.pop(0)
        all_text = last
        hing_texts = [last]
    else:
        history = episode
        all_text = " ".join(user_texts)
        hing_texts = user_texts
    regen = bool(payload.get("regen"))   # the user pressed "Regenerate"

    provider = PROVIDER
    if provider == "claude" and not has_api_key():
        provider = "demo"

    if provider == "demo":
        result = demo_reply(user_texts)
        result["demo"] = True
        return jsonify(result)

    if provider == "claude":
        try:
            result = normalize_claude(call_claude(history, n), all_text)
        except Exception as exc:
            print("Claude API error:", repr(exc))
            return jsonify({"mode": "error", "message": f"Sorry, I could not reach Claude: {exc}",
                            "steps": [], "verses": [], "demo": False})
        result["demo"] = False
        return jsonify(result)

    # ollama
    mode = "answer" if (n >= 4 or info_only) else "ask"
    if hinglish_chat(hing_texts):
        # the small model writes weak Hinglish, so the app uses fixed, well-written Hinglish text
        if mode == "ask":
            return jsonify({"mode": "ask", "message": HINGLISH_ASKS[min(n - 1, 2)], "steps": [],
                            "verses": [], "image_theme": None, "demo": False})
        message, steps = hinglish_answer(all_text)
        theme = detect_theme(all_text)
        return jsonify({"mode": "answer", "message": message, "steps": steps,
                        "verses": [verse_card(v) for v in pick_verses(theme, 2)],
                        "image_theme": scene_topic(all_text, info_only) or THEME_IMAGE.get(theme, "lotus"),
                        "demo": False})
    try:
        data = call_ollama(history, mode, n, regen)
    except Exception as exc:
        print("Ollama error:", repr(exc))
        return jsonify({"mode": "error", "steps": [], "verses": [], "demo": False,
                        "message": "I could not reach Ollama. Please make sure Ollama is running "
                                   "(open the Ollama app) and that you ran: ollama pull " + OLLAMA_MODEL})
    result = build_ollama_result(data, mode, all_text, info_only)
    result["demo"] = False
    return jsonify(result)


# ---------------------------------------------------------------- pages

@app.get("/")
def home_page():
    return send_from_directory(BASE_DIR / "static", "home.html")


@app.get("/chat")
def chat_page():
    return send_from_directory(BASE_DIR / "static", "index.html")


@app.get("/verses")
def verses_page():
    return send_from_directory(BASE_DIR / "static", "verses.html")


@app.get("/api/verses")
def api_verses():
    return jsonify(VERSES)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)