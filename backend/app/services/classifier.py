from app.services.llm_service import generate_response

# Supported feature categories in Language Learning Pal
VALID_FEATURES = [
    "VOCABULARY",
    "GRAMMAR",
    "TRANSLATION",
    "DAILY_PHRASES",
    "CONVERSATION",
    "PRONUNCIATION",
    "SYNONYMS",
    "ANTONYMS",
    "WORD_OF_DAY",
    "LEARNING_PLAN",
    "OUT_OF_DOMAIN"
]

# Classification prompt guidelines for LLM fallbacks
CLASSIFIER_PROMPT = """
You are a feature classification engine.

Classify the user's message into EXACTLY ONE category.

Categories:

VOCABULARY
GRAMMAR
TRANSLATION
DAILY_PHRASES
CONVERSATION
PRONUNCIATION
SYNONYMS
ANTONYMS
WORD_OF_DAY
LEARNING_PLAN
OUT_OF_DOMAIN

Classification Rules:

VOCABULARY:
Learning words, meanings, vocabulary building, advanced words, new words.

GRAMMAR:
Grammar correction, sentence correction, grammar checking, fixing sentences, grammatical mistakes.

TRANSLATION:
Translation requests between languages.

DAILY_PHRASES:
Daily communication phrases, office phrases, travel phrases, workplace communication.

CONVERSATION:
English speaking practice, conversation practice, chatting in English.

PRONUNCIATION:
Pronunciation help, speaking guidance, how to pronounce words.

SYNONYMS:
Similar words, alternative words.

ANTONYMS:
Opposite words.

WORD_OF_DAY:
Today's word, daily word, word of the day.

LEARNING_PLAN:
I want to improve English, roadmap, study plan, how to learn, study schedule.

OUT_OF_DOMAIN:
Anything unrelated to language learning.

Examples:

Message:
I am go to college everyday

Output:
GRAMMAR

Message:
Teach me 5 advanced English words

Output:
VOCABULARY

Message:
Give me today's word

Output:
WORD_OF_DAY

Message:
Translate hello to Telugu

Output:
TRANSLATION

Message:
Practice English with me

Output:
CONVERSATION

Message:
Who won IPL 2026?

Output:
OUT_OF_DOMAIN

Return ONLY the category name.
"""

def keyword_classifier(message: str) -> str:
    """
    Saves API call tokens by routing common keyword queries locally.
    """
    message = message.lower()

    vocabulary_keywords = [
        "vocabulary",
        "new words",
        "advanced words",
        "advanced english words",
        "english words",
        "teach me words",
        "teach me 5 words",
        "teach me english words",
        "learn words",
        "difficult words",
        "new vocabulary",
        "improve vocabulary"
    ]

    learning_plan_keywords = [
        "improve my english",
        "improve english",
        "learn english",
        "english roadmap",
        "learning plan",
        "study plan",
        "roadmap",
        "30 day plan"
    ]

    grammar_keywords = [
        "grammar",
        "correct",
        "fix",
        "correct my sentence",
        "sentence correction",
        "check grammar",
        "is this sentence correct"
    ]

    translation_keywords = [
        "translate",
        "translation",
        "meaning in",
        "convert to"
    ]

    phrase_keywords = [
        "daily phrases",
        "communication phrases",
        "office phrases",
        "travel phrases",
        "workplace phrases"
    ]

    conversation_keywords = [
        "practice english",
        "conversation",
        "chat with me",
        "speaking practice",
        "english practice"
    ]

    pronunciation_keywords = [
        "pronounce",
        "pronunciation",
        "how to pronounce"
    ]

    synonym_keywords = [
        "synonym",
        "synonyms",
        "similar words"
    ]

    antonym_keywords = [
        "antonym",
        "antonyms",
        "opposite word",
        "opposite words"
    ]

    word_day_keywords = [
        "word of the day",
        "today's word",
        "daily word",
        "new word today",
        "give me today's word",
        "today word"
    ]

    for keyword in vocabulary_keywords:
        if keyword in message:
            return "VOCABULARY"

    for keyword in grammar_keywords:
        if keyword in message:
            return "GRAMMAR"

    for keyword in translation_keywords:
        if keyword in message:
            return "TRANSLATION"

    for keyword in phrase_keywords:
        if keyword in message:
            return "DAILY_PHRASES"

    for keyword in conversation_keywords:
        if keyword in message:
            return "CONVERSATION"

    for keyword in pronunciation_keywords:
        if keyword in message:
            return "PRONUNCIATION"

    for keyword in synonym_keywords:
        if keyword in message:
            return "SYNONYMS"

    for keyword in antonym_keywords:
        if keyword in message:
            return "ANTONYMS"

    for keyword in word_day_keywords:
        if keyword in message:
            return "WORD_OF_DAY"

    for keyword in learning_plan_keywords:
        if keyword in message:
            return "LEARNING_PLAN"

    return "OUT_OF_DOMAIN"

def ai_classifier(message: str) -> str:
    """
    Queries LLM to classify unstructured or ambiguous inputs.
    """
    prompt = f"{CLASSIFIER_PROMPT}\n\nMessage:\n{message}\n"
    try:
        result = generate_response(prompt)
        result = result.strip().upper()
    except Exception:
        return "OUT_OF_DOMAIN"

    for feature in VALID_FEATURES:
        if feature in result:
            return feature

    return "OUT_OF_DOMAIN"

def classify_message(message: str) -> str:
    """
    Main entrypoint for classifying incoming messages.
    Uses local keyword search first, falling back to LLM processing.
    """
    feature = keyword_classifier(message)

    if feature != "OUT_OF_DOMAIN":
        return feature

    return ai_classifier(message)
