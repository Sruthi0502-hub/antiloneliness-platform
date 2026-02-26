"""
Sentimate Chatbot Module — Context-Aware, Bilingual (English + Tamil)
Provides warm, empathetic responses to elderly users.

Features:
- Name detection and personalised greetings
- Tamil and English keyword matching
- History-aware responses referencing previous messages
- Follow-up questions to keep conversation flowing
- Per-conversation context window from database history
"""
from ai_chatbot import get_ai_response
import re
import random
from ai_chatbot import get_ai_response
from typing import List, Dict, Optional, Any


# ============================================================
# RESPONSE LIBRARY — English
# ============================================================

EN_RESPONSES: Dict[str, List[str]] = {
    'greetings': [
        "Hello there! It's so wonderful to hear from you. How are you feeling today?",
        "Hello! I'm so glad you're here. What's on your mind?",
        "Hi! What a pleasure to chat with you today!",
        "Good to see you! How has your day been so far?",
        "Hello, my friend! I'm always happy to talk with you. How are you?",
        "Hi there! Lovely to have you here. How are you doing?",
        "Hello! I was just thinking — how wonderful it is to hear from you!",
        "Welcome! I'm so happy you stopped by. How are you feeling?",
    ],

    'status_check': [
        "I'm doing wonderfully, thank you for asking! How about yourself?",
        "I'm here and so happy to chat with you. How's your day been?",
        "I'm doing great! Tell me, how are you feeling today?",
        "I'm doing well, and I'm here for you. What's on your mind?",
        "I'm here for you, always! Is there something special you'd like to talk about?",
        "I'm doing wonderful! And you, my dear friend — how are you?",
        "I'm here and listening. What would you like to share with me today?",
    ],

    'emotional_support': [
        "I can hear that things feel difficult right now. You're not alone — I'm right here with you.",
        "It's okay to feel this way. Would you like to talk about what's on your heart?",
        "Loneliness can be very hard. Please know you are valued, cared for, and never truly alone.",
        "I'm here to listen, always. Sometimes just sharing how we feel makes the weight a little lighter.",
        "You are so important, and your feelings truly matter to me. I'm listening.",
        "Even on the hardest days, remember — you have worth, strength, and purpose.",
        "It takes courage to share your feelings. I'm proud of you for reaching out. Tell me more.",
        "I understand. It's not easy, but you don't have to carry this alone — I'm here.",
        "Your feelings are completely valid. I care about how you're doing. Can you tell me more?",
    ],

    'gratitude': [
        "You're very welcome! It's truly my pleasure to be here for you.",
        "Thank you for your kind words — they mean so much to me!",
        "I'm so happy I could help. Thank you for talking with me.",
        "You're so kind to say that! I'm here whenever you need me.",
        "I appreciate your gratitude. Helping you brings me such joy.",
        "You're welcome, my friend. I'm always here for you — never hesitate to reach out.",
        "It warms my heart to hear that. Thank you!",
    ],

    'encouragement': [
        "You're doing so well! Keep being your wonderful, amazing self.",
        "I believe in you with all my heart! You have so much to offer the world.",
        "That's truly wonderful — you should be very proud of yourself!",
        "What a great spirit you have! You inspire me every day.",
        "You are stronger than you know. Keep going — one step at a time!",
        "That's really commendable! You're making such a difference.",
        "I'm so proud of you. Every little effort you make matters enormously.",
    ],

    'memories': [
        "I'd love to hear about your memories! Do you have a favourite story to share?",
        "Memories are such a precious treasure. What's something you remember fondly?",
        "You must have so many wonderful life stories. Would you like to share one?",
        "Tell me about a happy moment from your life — I'd love to hear it.",
        "What's a memory that always makes you smile?",
        "I love hearing about your past. What comes to mind right now?",
        "Memories are gifts we carry with us. Share one with me?",
    ],

    'health': [
        "Your health is so important! Are you taking good care of yourself today?",
        "How's your health been lately? I hope you're feeling well.",
        "Remember to drink plenty of water and get some rest — your wellbeing matters so much!",
        "Have you taken your medications today? I care about your health.",
        "I hope you're being kind and gentle to yourself and your body.",
        "Taking good care of yourself is an act of self-love. That's truly wonderful!",
        "Your wellbeing is very important to me. Is there anything I can help with?",
    ],

    'family': [
        "Family is so precious. Would you like to tell me about someone special in your life?",
        "Relationships with loved ones are such a beautiful gift. How's your family doing?",
        "Who in your life means the most to you? I'd love to hear about them.",
        "Tell me about the people you love — I'm all ears!",
        "Your loved ones are so lucky to have you. How are your relationships?",
        "I'd love to hear about the people closest to your heart.",
        "Family stories are so wonderful. What would you like to share?",
    ],

    'happiness': [
        "That's wonderful to hear! What's making you feel so good today?",
        "How lovely! Your happiness makes me happy too. Tell me more!",
        "I'm so glad you're having a good day! What's been the best part?",
        "That's such good news! I love hearing this. Keep smiling!",
        "Your joy is contagious! What wonderful things are happening?",
    ],

    'name_received': [
        "What a beautiful name! It's a pleasure to meet you, {name}. How are you doing today?",
        "How lovely to meet you, {name}! I'll remember that. How has your day been?",
        "Oh, {name} — what a wonderful name! I'm so glad to know you. How are you feeling?",
        "Nice to meet you, {name}! I'm Sentimate, your companion. What's on your mind today?",
        "Hello, {name}! I'm so pleased to know your name now. How can I help you today?",
    ],

    'name_greeting': [
        "How are you doing today, {name}?",
        "It's so good to hear from you, {name}! What's on your mind?",
        "Hello, {name}! I've been looking forward to chatting with you. How are you?",
        "Good to see you again, {name}! How are you feeling today?",
    ],

    'conversation': [
        "I'd love to hear more about what you're thinking!",
        "Tell me more! I'm genuinely interested in what you have to say.",
        "That's really interesting — what else is on your mind?",
        "I'm listening! Please share more if you'd like.",
        "You have such interesting thoughts. Please continue!",
        "I love our conversations. What else would you like to talk about?",
        "Please continue — your thoughts are so valuable to me.",
    ],

    'default': [
        "That's an interesting thought! Tell me more about that.",
        "I appreciate you sharing that with me. How does it make you feel?",
        "That's something to think about. What else is on your mind?",
        "I'm here to listen, always — keep sharing.",
        "How can I help you feel better today?",
        "That sounds important to you. I'm right here with you.",
        "I understand. Is there something specific you'd like to talk through?",
        "Thank you for sharing that with me. How are you feeling right now?",
        "I value every single conversation we have. What else is on your heart?",
        "You're doing so well by opening up. Please keep going if you'd like.",
    ],
}


# ============================================================
# RESPONSE LIBRARY — Tamil (Unicode)
# ============================================================

TA_RESPONSES: Dict[str, List[str]] = {
    'greetings': [
        "வணக்கம்! உங்களிடம் பேசுவதற்கு மிகவும் மகிழ்ச்சியாக இருக்கிறது. இன்று எப்படி இருக்கிறீர்கள்?",
        "வணக்கம்! நான் இங்கே இருக்கிறேன். எப்படி உணர்கிறீர்கள்?",
        "வணக்கம் நண்பரே! இன்று என்ன நினைக்கிறீர்கள்?",
        "வணக்கம்! உங்களோடு பேசுவது மிகவும் மகிழ்ச்சியாக உள்ளது.",
        "வணக்கம்! இன்று எப்படி கழிக்கிறீர்கள்?",
    ],

    'status_check': [
        "நான் நன்றாக இருக்கிறேன், நன்றி! நீங்கள் எப்படி இருக்கிறீர்கள்?",
        "நான் மகிழ்ச்சியாக இருக்கிறேன். நீங்கள் எப்படி உணர்கிறீர்கள்?",
        "நான் உங்களுக்காக இங்கே இருக்கிறேன். இன்று என்ன விஷயம் பேசலாம்?",
        "நான் நல்லாவே இருக்கேன்! நீங்க?",
    ],

    'emotional_support': [
        "உங்கள் உணர்வுகளை புரிந்துகொள்கிறேன். நீங்கள் தனியாக இல்லை — நான் இங்கே இருக்கிறேன்.",
        "சில நேரங்களில் தனிமையாக உணர்வது இயல்பே. மனம் விட்டு பேசுங்கள்.",
        "உங்கள் வலி புரிகிறது. நான் கேட்கிறேன், கவலைப்படாதீர்கள்.",
        "நீங்கள் மதிப்புமிக்கவர். உங்கள் உணர்வுகள் முக்கியமானவை.",
        "துணிச்சலுடன் உள்ளதை சொன்னதற்கு நன்றி. தொடர்ந்து பேசுங்கள்.",
    ],

    'gratitude': [
        "மிக்க நன்றி! உங்களுக்கு உதவுவது என் மகிழ்ச்சி.",
        "நன்றி! உங்களுடன் பேசுவது எனக்கு மிகவும் மகிழ்ச்சியாக உள்ளது.",
        "நன்றி நண்பரே! எப்போதும் இங்கே இருக்கிறேன்.",
        "உங்கள் அன்பான வார்த்தைகளுக்கு நன்றி!",
    ],

    'encouragement': [
        "நீங்கள் மிகவும் நன்றாக செய்கிறீர்கள்! தொடர்ந்து முன்னேறுங்கள்.",
        "உங்களில் நம்பிக்கை வைக்கிறேன். நீங்கள் சக்தியானவர்!",
        "அருமை! இதற்காக நீங்கள் பெருமைப்படலாம்.",
        "உங்கள் மனோதிடம் என்னை ஊக்கப்படுத்துகிறது!",
    ],

    'memories': [
        "உங்கள் நினைவுகளைப் பற்றி கேட்க விரும்புகிறேன்! ஒரு கதை சொல்லுங்கள்.",
        "நினைவுகள் மிக விலைமதிப்பற்றவை. ஒரு மகிழ்ச்சியான தருணம் சொல்லுங்கள்.",
        "உங்கள் வாழ்க்கையில் எந்த நினைவு எப்போதும் சிரிக்க வைக்கிறது?",
    ],

    'health': [
        "உங்கள் உடல்நலம் மிகவும் முக்கியம்! நன்றாக கவனித்துக்கொள்கிறீர்களா?",
        "இன்று மருந்து சாப்பிட்டீர்களா? உங்கள் ஆரோக்கியம் முக்கியம்.",
        "தண்ணீர் குடிக்கவும், சரியாக தூங்கவும் மறவாதீர்கள்!",
        "உங்கள் உடல்நலம் எப்படி இருக்கிறது? நான் கவலைப்படுகிறேன்.",
    ],

    'family': [
        "குடும்பம் மிகவும் விலைமதிப்பற்றது. யாராவது விஷேஷமானவர்களைப் பற்றி சொல்லுங்கள்.",
        "உங்கள் குடும்பத்தினர் எப்படி இருக்கிறார்கள்?",
        "உங்கள் மனதிற்கு நெருங்கியவர்களைப் பற்றி சொல்ல விரும்புகிறேன்.",
    ],

    'happiness': [
        "மிகவும் மகிழ்ச்சியாக இருக்கிறது கேட்கவே! என்ன நடந்தது?",
        "உங்கள் மகிழ்ச்சி எனக்கும் மகிழ்ச்சியே! என்ன விஷேஷம்?",
        "அருமை! தொடர்ந்து சிரித்துக்கொண்டே இருங்கள்!",
    ],

    'name_received': [
        "{name} என்ற பெயர் மிக அழகானது! மகிழ்ச்சியாக இருக்கிறது. இன்று எப்படி இருக்கிறீர்கள்?",
        "ஓ, {name}! தெரிந்துகொண்டதற்கு மகிழ்ச்சி. நான் Sentimate. என்ன நினைக்கிறீர்கள்?",
    ],

    'name_greeting': [
        "நலமாக இருக்கிறீர்களா, {name}?",
        "{name}! நீங்கள் வந்தது மகிழ்ச்சி. இன்று என்ன விஷயம்?",
    ],

    'default': [
        "சுவாரஸ்யமான கருத்து! இன்னும் சொல்லுங்கள்.",
        "புரிகிறது. எப்படி உணர்கிறீர்கள்?",
        "நான் கேட்கிறேன். மனம் விட்டு பேசுங்கள்.",
        "உங்கள் எண்ணங்கள் முக்கியமானவை. தொடருங்கள்.",
        "இன்று எப்படி உதவலாம்?",
        "நன்றி! இன்னும் என்ன நினைக்கிறீர்கள்?",
    ],
}


# ============================================================
# KEYWORD MAPPINGS
# ============================================================

# English keywords → category
EN_KEYWORDS: Dict[str, str] = {
    # Greetings
    'hello': 'greetings', 'hi': 'greetings', 'hey': 'greetings',
    'good morning': 'greetings', 'good evening': 'greetings',
    'good afternoon': 'greetings', 'greetings': 'greetings',

    # Status
    'how are you': 'status_check', 'how do you do': 'status_check',
    'how have you been': 'status_check', 'are you okay': 'status_check',

    # Emotional
    'lonely': 'emotional_support', 'loneliness': 'emotional_support',
    'sad': 'emotional_support', 'depressed': 'emotional_support',
    'unhappy': 'emotional_support', 'upset': 'emotional_support',
    'worried': 'emotional_support', 'anxiety': 'emotional_support',
    'anxious': 'emotional_support', 'scared': 'emotional_support',
    'afraid': 'emotional_support', 'hurt': 'emotional_support',
    'crying': 'emotional_support', 'miss': 'emotional_support',
    'grief': 'emotional_support', 'low': 'emotional_support',

    # Gratitude
    'thank you': 'gratitude', 'thank': 'gratitude', 'thanks': 'gratitude',
    'appreciate': 'gratitude', 'grateful': 'gratitude',

    # Encouragement
    'accomplished': 'encouragement', 'achievement': 'encouragement',
    'proud': 'encouragement', 'success': 'encouragement',
    'happy': 'happiness', 'great': 'happiness', 'wonderful': 'happiness',
    'excited': 'happiness', 'joyful': 'happiness', 'joy': 'happiness',
    'good news': 'happiness', 'fantastic': 'happiness',

    # Memories
    'remember': 'memories', 'memory': 'memories', 'memories': 'memories',
    'long ago': 'memories', 'old days': 'memories', 'when i was': 'memories',
    'the past': 'memories', 'used to': 'memories',

    # Health
    'health': 'health', 'medicine': 'health', 'medication': 'health',
    'doctor': 'health', 'hospital': 'health', 'exercise': 'health',
    'eating': 'health', 'sleep': 'health', 'pain': 'health',
    'sick': 'health', 'illness': 'health',

    # Family
    'family': 'family', 'mother': 'family', 'father': 'family',
    'children': 'family', 'grandchild': 'family', 'grandchildren': 'family',
    'husband': 'family', 'wife': 'family', 'son': 'family',
    'daughter': 'family', 'loved one': 'family', 'spouse': 'family',
    'grandson': 'family', 'granddaughter': 'family',
}

# Tamil keywords → category (keyword is substring of Tamil message)
TA_KEYWORDS: Dict[str, str] = {
    'வணக்கம்': 'greetings',
    'ஹலோ': 'greetings',
    'காலை வணக்கம்': 'greetings',
    'மாலை வணக்கம்': 'greetings',
    'நீங்கள் எப்படி': 'status_check',
    'எப்படி இருக்கிறீர்கள்': 'status_check',
    'எப்படி இருக்க': 'status_check',
    'தனிமை': 'emotional_support',
    'சோகம்': 'emotional_support',
    'கஷ்டம்': 'emotional_support',
    'வலிக்கிறது': 'emotional_support',
    'கஷ்டமாக': 'emotional_support',
    'அழுகிறேன்': 'emotional_support',
    'நன்றி': 'gratitude',
    'மிக்க நன்றி': 'gratitude',
    'சந்தோஷம்': 'happiness',
    'மகிழ்ச்சி': 'happiness',
    'குடும்பம்': 'family',
    'அம்மா': 'family',
    'அப்பா': 'family',
    'பிள்ளைகள்': 'family',
    'பேரன்': 'family',
    'பேத்தி': 'family',
    'நினைவு': 'memories',
    'பழைய நாட்கள்': 'memories',
    'உடல்நலம்': 'health',
    'மருந்து': 'health',
    'டாக்டர்': 'health',
    'என் பெயர்': 'name_intro_ta',
    'என்னை': 'name_intro_ta',
}

# ============================================================
# FOLLOW-UP QUESTIONS  (appended to responses to keep the
# conversation going in both languages)
# ============================================================

EN_FOLLOWUPS = [
    " What else is on your mind today?",
    " How are you feeling overall?",
    " Is there anything else you'd like to share?",
    " What would you like to talk about next?",
    " Is there something I can do to make your day better?",
    " Would you like to tell me more?",
]

TA_FOLLOWUPS = [
    " இன்னும் என்ன நினைக்கிறீர்கள்?",
    " வேறு என்ன பேசலாம்?",
    " நான் வேறு எதாவது உதவலாமா?",
    " இன்னும் சொல்ல விரும்புகிறீர்களா?",
]


# ============================================================
# NAME EXTRACTION
# ============================================================

_NAME_PATTERNS = [
    # English
    r"my name is ([A-Za-z]+)",
    r"i am ([A-Za-z]+)",
    r"i'm ([A-Za-z]+)",
    r"call me ([A-Za-z]+)",
    r"name'?s? ([A-Za-z]+)",
    # Tamil (approximate romanised detection)
    r"என் பெயர் ([^\s]+)",
    r"என்னை ([^\s]+) என்று",
]

def _extract_name(message: str) -> Optional[str]:
    """Try to extract a proper name from the user's message."""
    # Skip common non-name words that follow "I am"
    skip_words = {
        'fine', 'ok', 'okay', 'good', 'great', 'doing', 'well',
        'sad', 'happy', 'here', 'back', 'ready', 'not', 'feeling',
        'a', 'an', 'the', 'just', 'so', 'very', 'now', 'still',
    }
    for pattern in _NAME_PATTERNS:
        m = re.search(pattern, message, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip().capitalize()
            if candidate.lower() not in skip_words and len(candidate) >= 2:
                return candidate
    return None


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def _is_tamil(message: str) -> bool:
    """Return True if message contains Tamil Unicode characters."""
    return any('\u0B80' <= ch <= '\u0BFF' for ch in message)


# ============================================================
# KEYWORD MATCHING
# ============================================================

def _match_category(message_lower: str, is_tamil: bool) -> str:
    """Find best matching response category; longest keyword wins."""
    keyword_map = TA_KEYWORDS if is_tamil else EN_KEYWORDS

    # Sort by keyword length descending (most specific match first)
    for kw, cat in sorted(keyword_map.items(), key=lambda x: len(x[0]), reverse=True):
        if kw in message_lower:
            return cat

    # If Tamil text but no keyword matched, still use Tamil default
    return 'default'


# ============================================================
# HISTORY ANALYSIS
# ============================================================

def _analyse_history(history: List[Dict]) -> Optional[str]:
    """
    Scan recent user messages for a dominant emotional tone.
    Returns a short acknowledgement phrase or None.
    """
    emotional_kws = {
        'lonely': "lonely", 'loneliness': "lonely",
        'sad': "sad", 'depressed': "sad", 'unhappy': "sad",
        'worried': "worried", 'anxious': "worried",
        'scared': "scared", 'happy': "happy", 'joy': "happy",
    }
    tone_counts: Dict[str, int] = {}

    for msg in history[-6:]:  # look at last 6 messages
        if msg.get('sender') != 'user':
            continue
        text = msg.get('message', '').lower()
        for kw, tone in emotional_kws.items():
            if kw in text:
                tone_counts[tone] = tone_counts.get(tone, 0) + 1

    if not tone_counts:
        return None

    dominant = max(tone_counts, key=tone_counts.get)
    phrases = {
        'lonely':  "I remember you mentioned feeling lonely earlier — I want you to know I'm here. ",
        'sad':     "I noticed you've been feeling a bit down — I hope this conversation helps. ",
        'worried': "I know things have felt worrying lately — remember you don't have to face it alone. ",
        'scared':  "It sounds like things have been a little scary. I'm right here with you. ",
        'happy':   "It's so lovely that you've been in good spirits! ",
    }
    return phrases.get(dominant)


# ============================================================
# PUBLIC API
# ============================================================

def get_response(
    user_message: str,
    username: Optional[str] = None,
    history: Optional[List[Dict]] = None,
    display_name: Optional[str] = None,
    forced_language: Optional[str] = None,
) -> Dict[str, Any]:

    """
    Generate a warm, context-aware chatbot response.
    """

    if not isinstance(user_message, str):
        raise ValueError("message must be a string")

    message = user_message.strip()

    if not message:
        return {
            "response": "I'm here to listen. Feel free to share whatever's on your mind! 💚",
            "detected_name": None,
            "language": "english",
        }

    # Language detection
    is_tamil = True if forced_language == 'tamil' else _is_tamil(message)

    message_lower = message.lower()
    history = history or []

    responses = TA_RESPONSES if is_tamil else EN_RESPONSES
    followups = TA_FOLLOWUPS if is_tamil else EN_FOLLOWUPS

    lang = "tamil" if is_tamil else "english"

    # 1️⃣ Name extraction
    detected_name = _extract_name(message)

    effective_name = detected_name or display_name

    # 2️⃣ Category detection
    category = _match_category(message_lower, is_tamil)

    if category == 'name_intro_ta' and detected_name:
        category = 'name_received'

    # 3️⃣ Base response selection

    if category == 'name_received' and detected_name:

        pool = responses.get('name_received', responses['default'])

        base = random.choice(pool).format(name=detected_name)

    elif category == 'greetings' and effective_name:

        if random.random() < 0.55:

            pool = responses.get('name_greeting', responses['greetings'])

            base = random.choice(pool).format(name=effective_name)

        else:

            base = random.choice(
                responses.get('greetings', responses['default'])
            )

    else:

        pool = responses.get(category, responses['default'])

        base = random.choice(pool)

    # 4️⃣ History awareness

    history_note = _analyse_history(history) if len(history) >= 3 else None

    prefix = ""

    if history_note and random.random() < 0.35:

        prefix = history_note

    # 5️⃣ Follow-up question

    followup = ""

    if not base.rstrip().endswith('?'):

        if random.random() < 0.75:

            followup = " " + random.choice(followups)

    # 6️⃣ AI Integration

    ai_reply = get_ai_response(message, username)

    # 7️⃣ Final response

    response_text = prefix + base + " " + ai_reply + followup

    return {

        "response": response_text,

        "detected_name": detected_name,

        "language": lang,

    }