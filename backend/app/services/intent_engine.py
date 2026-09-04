"""
===========================================================
LANGUAGE LEARNING PAL INTENT ENGINE
Version: 2.0

Responsibilities:
- Intent Classification
- Multi Intent Detection
- Goal Extraction
- Entity Extraction
- Confidence Scoring
- LLM Fallback Classification

===========================================================
"""

import re
from collections import Counter

from app.models.intent_result import IntentResult


class IntentEngine:

    INTENT_PATTERNS = {

        "GRAMMAR": [
            "grammar",
            "correct",
            "fix sentence",
            "sentence correction",
            "grammar mistake",
            "is this sentence correct"
        ],

        "VOCABULARY": [
            "meaning",
            "word meaning",
            "vocabulary",
            "new word",
            "define",
            "definition"
        ],

        "TRANSLATION": [
            "translate",
            "translation",
            "translate into",
            "translate to"
        ],

        "PRONUNCIATION": [
            "pronunciation",
            "pronounce",
            "how to pronounce",
            "ipa"
        ],

        "CONVERSATION": [
            "conversation",
            "speaking",
            "chat with me",
            "practice speaking",
            "roleplay"
        ],

        "LEARNING_PLAN": [
            "plan",
            "roadmap",
            "schedule",
            "learning path",
            "study plan",
            "30 day plan",
            "learning plan",
            "learn english",
            "improve english",
            "improve my english",
            "english plan",
            "study english",
            "speak english",
            "english roadmap",
            "learn communication",
            "become fluent",
            "improve communication",
            "improve pronunciation",
            "improve grammar"
        ],

        "SYNONYMS": [
            "synonym",
            "similar word"
        ],

        "ANTONYMS": [
            "antonym",
            "opposite word"
        ],

        "WORD_OF_DAY": [
    "word of the day",
    "today's word",
    "word today",
    "daily word"
],

"CULTURAL": [
    "cultural",
    "culture",
    "cultural meaning",
    "cultural context",
    "cultural significance",
    "when is this used",
    "how is this used culturally",
    "is this culturally appropriate",
    "cultural usage",
    "social context"
]
    }

    GOAL_PATTERNS = [
        "improve",
        "learn",
        "master",
        "practice",
        "become fluent",
        "prepare for",
        "develop"
    ]

    ENTITY_PATTERNS = {

        "LANGUAGE": [
            "english",
            "telugu",
            "hindi",
            "french",
            "spanish"
        ],

        "SKILL": [
            "grammar",
            "vocabulary",
            "pronunciation",
            "speaking",
            "conversation",
            "communication"
        ]
    }

    @classmethod
    def classify_intent(cls, message: str):

        text = re.sub(r'[\\/?.!\'"’`\s]+$', '', message.lower().strip())

        # RESET_PROGRESS check
        reset_progress_patterns = [
            "reset my learning progress to day 1",
            "reset my progress",
            "reset learning plan",
            "reset plan",
            "restart 30-day plan",
            "restart plan",
            "reset progress",
            "reset"
        ]
        if any(pat in text for pat in reset_progress_patterns):
            return IntentResult(
                intent="RESET_PROGRESS",
                confidence=1.0
            )

        # COMPLETE_DAY check
        complete_day_patterns = [
            "i completed today's task",
            "completed today's task",
            "i finished today's task",
            "finished today's task",
            "complete today's task"
        ]
        if any(pat in text for pat in complete_day_patterns):
            return IntentResult(
                intent="COMPLETE_DAY",
                confidence=1.0
            )

        # CONTINUE_PLAN check
        continue_plan_patterns = [
            "continue my learning plan",
            "continue learning plan",
            "continue plan",
            "continue learning",
            "next day"
        ]
        if any(pat in text for pat in continue_plan_patterns):
            return IntentResult(
                intent="CONTINUE_PLAN",
                confidence=1.0
            )

        # SHOW_CURRENT_DAY check
        show_current_day_patterns = [
            "what day am i on",
            "what day is it",
            "what's my day",
            "current day",
            "which day am i on",
            "what day am i"
        ]
        if any(pat in text for pat in show_current_day_patterns):
            return IntentResult(
                intent="SHOW_CURRENT_DAY",
                confidence=1.0
            )

        # SHOW_ROADMAP check
        show_roadmap_patterns = [
            "show my roadmap",
            "what is my roadmap",
            "my roadmap",
            "show roadmap",
            "view roadmap",
            "what is the roadmap"
        ]
        if any(pat in text for pat in show_roadmap_patterns):
            return IntentResult(
                intent="SHOW_ROADMAP",
                confidence=1.0
            )

        # SHOW_PROGRESS check
        show_progress_patterns = [
            "show my progress",
            "what is my progress",
            "progress update",
            "my progress",
            "show progress",
            "track progress"
        ]
        if any(pat in text for pat in show_progress_patterns):
            return IntentResult(
                intent="SHOW_PROGRESS",
                confidence=1.0
            )

        # Learning plan priority check
        learning_plan_patterns = [
            "create roadmap",
            "create learning plan",
            "generate roadmap",
            "generate plan",
            "study plan",
            "what should i study",
            "what should i learn today",
            "what should i do today",
            "what to do today",
            "what should i do",
            "today's task",
            "today's exercises",
            "today's lesson",
            "based on my goal",
            "based on my profile",
            "using my profile",
            "30 day roadmap",
            "30-day plan",
            "30 day plan",
            "roadmap",
            "learning plan",
            "learning path",
            "i want to learn english",
            "i want to improve english",
            "i want to improve my english",
            "improve english",
            "improve my english",
            "learn english",
            "english roadmap",
            "learning roadmap",
            "become fluent",
            "improve communication",
            "improve pronunciation",
            "improve grammar"
        ]
        if any(pat in text for pat in learning_plan_patterns):
            return IntentResult(
                intent="LEARNING_PLAN",
                confidence=1.0
            )

        # Progress query check
        progress_query_patterns = [
            "show my progress",
            "what is my progress",
            "my progress",
            "show progress",
            "track progress",
            "completed lessons",
            "overall progress",
            "completed tasks"
        ]
        if any(pat in text for pat in progress_query_patterns):
            return IntentResult(
                intent="PROGRESS_QUERY",
                confidence=1.0
            )

        # Memory query check
        memory_query_patterns = [
            "what are my weak areas",
            "what is my goal",
            "what is my current profile",
            "what is my profile",
            "my profile",
            "show my profile",
            "what is my weak area",
            "my weak areas",
            "what are my goals",
            "my current profile",
            "show profile"
        ]
        if any(pat in text for pat in memory_query_patterns):
            return IntentResult(
                intent="MEMORY_QUERY",
                confidence=1.0
            )

        # Profile update check
        profile_update_patterns = [
            "my goal is",
            "my target is",
            "i want placement",
            "placements",
            "my objective is",
            "my weak area is",
            "my weak areas are",
            "i am a beginner",
            "i am an intermediate",
            "i am advanced",
            "i'm a beginner",
            "i'm intermediate",
            "i'm advanced"
        ]
        if any(pat in text for pat in profile_update_patterns):
            return IntentResult(
                intent="PROFILE_UPDATE",
                confidence=1.0
            )

        scores = Counter()

        for intent, patterns in cls.INTENT_PATTERNS.items():

            for pattern in patterns:

                if pattern in text:
                    scores[intent] += 1

        if not scores:

            return IntentResult(
                intent="OUT_OF_DOMAIN",
                confidence=0.0
            )

        best_intent = scores.most_common(1)[0][0]

        highest_score = scores[best_intent]

        confidence = round(
            min(highest_score / 3.0, 1.0),
            2
        )

        return IntentResult(
            intent=best_intent,
            confidence=confidence
        )

    @classmethod
    def detect_multi_intents(cls, message: str):

        text = message.lower()

        detected = []

        for intent, patterns in cls.INTENT_PATTERNS.items():

            for pattern in patterns:

                if pattern in text:
                    detected.append(intent)
                    break

        return list(set(detected))

    @classmethod
    def extract_entities(cls, message: str):

        text = message.lower()

        entities = []

        for entity_type, values in cls.ENTITY_PATTERNS.items():

            for value in values:

                if value in text:

                    entities.append({
                        "type": entity_type,
                        "value": value
                    })

        return entities

    @classmethod
    def extract_goal(cls, message: str):

        text = message.lower()

        for pattern in cls.GOAL_PATTERNS:

            if pattern in text:
                return message

        return ""

    @classmethod
    def detect_learning_level(cls, message: str):

        text = message.lower()

        if "beginner" in text:
            return "Beginner"

        if "intermediate" in text:
            return "Intermediate"

        if "advanced" in text:
            return "Advanced"

        return "Unknown"

    @classmethod
    def detect_duration(cls, message: str):

        match = re.search(
            r"(\d+)\s*(day|days|week|weeks|month|months)",
            message.lower()
        )

        if match:
            return match.group()

        return ""

    @classmethod
    def analyze(cls, message: str):

        result = cls.classify_intent(message)

        result.tasks = cls.detect_multi_intents(message)

        result.entities = cls.extract_entities(message)

        result.goal = cls.extract_goal(message)

        result.learning_level = cls.detect_learning_level(message)

        result.duration = cls.detect_duration(message)

        return result