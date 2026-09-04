"""
===========================================================
LANGUAGE LEARNING PAL DOMAIN CONFIGURATION

Defines:

1. Domain Boundaries
2. Learning Categories
3. Intent Mapping
4. Tool Mapping
5. Out-of-Domain Topics
6. Supported User Goals

===========================================================
"""

# ==========================================================
# PRIMARY DOMAIN
# ==========================================================

PRIMARY_DOMAIN = "Language Learning"

# ==========================================================
# IN-DOMAIN TOPICS
# ==========================================================

IN_DOMAIN_TOPICS = [

    "grammar",

    "vocabulary",

    "translation",

    "pronunciation",

    "speaking",

    "conversation",

    "communication",

    "english learning",

    "daily phrases",

    "word meanings",

    "synonyms",

    "antonyms",

    "language improvement",

    "fluency",

    "writing skills",

    "reading skills",

    "listening skills",

    "interview english",

    "public speaking",

    "business communication"
]

# ==========================================================
# OUT OF DOMAIN TOPICS
# ==========================================================

OUT_OF_DOMAIN_TOPICS = [

    "medical diagnosis",

    "stock prediction",

    "crypto prediction",

    "sports prediction",

    "ipl",

    "betting",

    "gambling",

    "politics",

    "religious debates",

    "hacking",

    "malware",

    "cyber attacks",

    "weapons",

    "illegal activities",

    "adult content",

    "financial investment advice",

    "legal advice"
]

# ==========================================================
# SUPPORTED LEARNING CATEGORIES
# ==========================================================

LEARNING_CATEGORIES = [

    "Grammar",

    "Vocabulary",

    "Translation",

    "Pronunciation",

    "Conversation",

    "Daily Phrases",

    "Writing",

    "Reading",

    "Listening",

    "Communication Skills"
]

# ==========================================================
# SUPPORTED USER GOALS
# ==========================================================

SUPPORTED_GOALS = [

    "Improve English",

    "Improve Grammar",

    "Build Vocabulary",

    "Improve Pronunciation",

    "Practice Conversations",

    "Prepare For Interviews",

    "Improve Communication Skills",

    "Business English",

    "Daily Communication",

    "Public Speaking"
]

# ==========================================================
# INTENT TO CATEGORY MAPPING
# ==========================================================

INTENT_CATEGORY_MAP = {

    "GRAMMAR": "Grammar",

    "VOCABULARY": "Vocabulary",

    "TRANSLATION": "Translation",

    "PRONUNCIATION": "Pronunciation",

    "CONVERSATION": "Conversation",

    "LEARNING_PLAN": "Learning Plan",

    "SYNONYMS": "Vocabulary",

    "ANTONYMS": "Vocabulary",

    "WORD_OF_DAY": "Vocabulary",

    "PROGRESS_TRACKING": "Progress",

    "MULTI_TASK": "Multiple Learning Tasks",

    "OUT_OF_DOMAIN": "Unsupported"
}

# ==========================================================
# TOOL ROUTING MAP
# ==========================================================

INTENT_TOOL_MAP = {

    "VOCABULARY": "dictionary_tool",

    "TRANSLATION": "translation_tool",

    "PRONUNCIATION": "pronunciation_tool",

    "WORD_OF_DAY": "dictionary_tool",

    "SYNONYMS": "dictionary_tool",

    "ANTONYMS": "dictionary_tool"
}

# ==========================================================
# LEARNING LEVELS
# ==========================================================

LEARNING_LEVELS = [

    "Beginner",

    "Intermediate",

    "Advanced"
]

# ==========================================================
# AGENT RECOMMENDATIONS
# ==========================================================

RECOMMENDED_FEATURES = {

    "Beginner": [
        "Vocabulary",
        "Daily Phrases",
        "Translation"
    ],

    "Intermediate": [
        "Grammar",
        "Conversation",
        "Pronunciation"
    ],

    "Advanced": [
        "Business English",
        "Public Speaking",
        "Interview Practice"
    ]
}

# ==========================================================
# OUT OF DOMAIN RESPONSE
# ==========================================================

OUT_OF_DOMAIN_RESPONSE = """
I am Language Learning Pal, a Language Learning Agent.

I specialize in:

• Grammar Correction
• Vocabulary Building
• Translation
• Pronunciation Guidance
• Conversation Practice
• Learning Plans

Please ask a language-learning related question.
"""