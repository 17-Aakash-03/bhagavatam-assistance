"""Hand-written Hinglish answers.

The small local model writes weak Hinglish, so for Hinglish chats the app builds the
answer from sentences written and checked in advance. Only ideas from the verified
Bhagavatam list are attributed to the Bhagavatam.
"""
import re

# theme -> words (single words, lowercase) that suggest it, in priority order
THEME_WORDS = [
    ("loss", {"guzar", "guzarna", "nidhan", "mrityu", "death", "died", "passed", "chal", "yaad"}),
    ("study", {"exam", "marks", "result", "fail", "padhai", "padh", "padhna", "padhte", "college",
               "school", "percentage", "backlog", "paper", "board", "neet", "jee"}),
    ("work", {"kaam", "office", "boss", "job", "naukri", "career", "interview", "salary", "project"}),
    ("relation", {"breakup", "pyaar", "pyar", "rishta", "girlfriend", "boyfriend", "partner",
                  "shaadi", "biwi", "pati", "dhokha"}),
    ("family", {"ghar", "mummy", "papa", "parents", "ladai", "ladte", "family", "bhai", "behen"}),
    ("lonely", {"akela", "akele", "akelapan", "lonely", "dost"}),
    ("anxiety", {"ghabrahat", "ghabra", "ghabrata", "darr", "dar", "chinta", "tension", "stress",
                 "stressed", "anxious", "anxiety", "bechaini"}),
    ("anger", {"gussa", "gusse", "chidchida", "jalan", "irritate"}),
]

OPENERS = {
    "loss": "Apne kisi priyajan ko khone ka dard bahut gehra hota hai, aur aansoo bahana swabhavik hai.",
    "study": "Exam ya marks ka dabav bahut bhaari lagta hai, par ek result aapki keemat tay nahi karta.",
    "work": "Kaam ka dabav lambe samay tak rahe to insaan thak jaata hai, aur yeh thakan kamzori nahi hai.",
    "relation": "Rishton ka dard gehra hota hai, aur use mehsoos karna bilkul swabhavik hai.",
    "family": "Ghar ka tanav sabse zyada chubhta hai, kyunki wahi hamari sabse apni jagah hoti hai.",
    "lonely": "Akelapan bahut bhaari lagta hai, aur ismein aapki koi galti nahi hai.",
    "anxiety": "Ghabrahat aur chinta bahut thaka deti hain, aur aap isme akele nahi hain.",
    "anger": "Gussa aksar tab badhta hai jab hamari ummeedein tootti hain, aur ise pehchanna achhi shuruaat hai.",
    "sad": "Udaasi ka bojh uthana mushkil hota hai, aur ise batane ki himmat karna achhi baat hai.",
}

# only ideas from the verified Bhagavatam list
IDEAS = {
    "loss": "Bhagavatam kathinaiyon ko dhairya aur vinamrata ke saath sweekar karne ki baat karta hai, "
            "aur achhe logon ki sangat ko hriday ke liye poshan batata hai.",
    "study": "Bhagavatam yaad dilata hai ki jeevan chhota hai aur har din keemti hai, "
             "isliye aaj ka ek chhota kadam bhi sarthak hai.",
    "work": "Bhagavatam yaad dilata hai ki jeevan chhota hai aur har din keemti hai, "
            "isliye apni sehat aur samay ki raksha karna zaroori hai.",
    "relation": "Bhagavatam kathinaiyon ko dhairya aur vinamrata ke saath sweekar karne ki baat karta hai, "
                "aur achhe logon ki sangat ko hriday ke liye poshan batata hai.",
    "family": "Bhagavatam achhe logon ki sangat ko hriday ke liye poshan batata hai, "
              "isliye ek bharose ke vyakti se baat karna madad kar sakta hai.",
    "lonely": "Bhagavatam achhe logon ki sangat ko hriday ke liye poshan batata hai, "
              "isliye achhe logon se milne ke chhote kadam bahut kaam aate hain.",
    "anxiety": "Bhagavatam sikhata hai ki darr tab aata hai jab hum apni asli pehchan bhool kar "
               "asthaayi sharir ko hi swayam maan lete hain.",
    "anger": "Bhagavatam sikhata hai ki bhautik sukhon ki lalsa gehra dukh deti hai "
             "aur use chhodne se shanti milti hai.",
    "sad": "Bhagavatam kathinaiyon ko dhairya aur vinamrata ke saath sweekar karne ki baat karta hai, "
           "aur achhe logon ki sangat ko hriday ke liye poshan batata hai.",
}

CLOSING = "Chhote kadamon se shuru kijiye aur kisi bharose ke vyakti se apni baat zaroor kijiye."

THEME_STEPS = {
    "loss": ["Apne priyajan ki koi yaad ghar ke kisi apne ke saath baantiye.",
             "Khud ko dukh mehsoos karne ka samay dijiye, jaldi theek hone ka dabav mat daaliye."],
    "study": ["Padhai ko chhote hisson mein baant kar roz ek hissa poora kijiye.",
              "Apne marks ya result ke baare mein kisi teacher ya senior se baat kijiye."],
    "work": ["Apne kaam ki list banakar sabse zaroori kaam pehle kijiye.",
             "Kaam ke beech chhoti si sair ya kuch minute shaanti se baithiye."],
    "relation": ["Apni feeling ek diary mein likhiye, bina kisi ko dosh diye.",
                 "Kisi bharose ke dost se milkar apna dukh baantiye."],
    "family": ["Kisi ek bharose ke rishtedaar ya dost se apni baat batayiye.",
               "Shaant samay chunkar apni feeling bina dosh diye ghar mein rakhiye."],
    "lonely": ["Roz ek vyakti ko hello kijiye ya do minute baat kijiye.",
               "Kisi club, satsang ya samooh se judne ki koshish kijiye."],
    "anxiety": ["4 ginti tak saans andar aur 6 ginti tak bahar chhodiye, paanch baar.",
                "Jis cheez ki chinta hai use kaagaz par likhiye aur ek chhota kadam chuniye."],
    "anger": ["Gussa aaye to ek gilaas paani peeyiye aur dus tak ginti kijiye.",
              "Shaant hone ke baad apni baat saaf shabdon mein rakhiye."],
    "sad": ["Aaj ek chhota kaam chuniye jo aapko achha lagta ho, jaise sair ya sangeet.",
            "Apni feeling kaagaz par likh dijiye."],
}

SLEEP_WORDS = {"neend", "sona", "sota", "soti", "so", "jaagta", "jaagti", "raat"}
FOOD_WORDS = {"khana", "bhookh", "bhook", "skip", "nashta", "lunch", "khaata", "khati"}

STEP_SLEEP = "Sone aur uthne ka samay tay kijiye aur sone se ek ghanta pehle phone door rakhiye."
STEP_FOOD = "Niyamit samay par khana khaiye, khana skip mat kijiye."
STEP_BOTH = "Niyamit samay par khana khaiye aur sone-uthne ka samay tay kijiye, phone sone se pehle door rakhiye."
STEP_ROUTINE = "Neend aur khane ka ek niyamit routine banaiye."
STEP_PRAYER = "Roz paanch minute shaanti se prarthna ya naam-jap kijiye."
STEP_DOCTOR = "Agar yeh kai hafton tak rahe to doctor ya counsellor se zaroor baat kijiye."


def _tokens(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def detect_hinglish_theme(text):
    tokens = _tokens(text)
    for theme, words in THEME_WORDS:
        if tokens & words:
            return theme
    return "sad"


def hinglish_answer(all_text):
    """Return (message, steps) for a Hinglish chat."""
    theme = detect_hinglish_theme(all_text)
    tokens = _tokens(all_text)
    message = " ".join([OPENERS[theme], IDEAS[theme], CLOSING])

    if tokens & SLEEP_WORDS and tokens & FOOD_WORDS:
        care = STEP_BOTH
    elif tokens & SLEEP_WORDS:
        care = STEP_SLEEP
    elif tokens & FOOD_WORDS:
        care = STEP_FOOD
    else:
        care = STEP_ROUTINE

    steps = list(THEME_STEPS[theme]) + [care, STEP_PRAYER, STEP_DOCTOR]
    return message, steps