"""
===========================================================
LANGUAGE LEARNING PAL REFLECTION ENGINE
Version: 2.0

Purpose:
- Self Evaluation
- Response Validation
- Quality Assessment
- Confidence Scoring
- Improvement Suggestions

Architecture:

Response
    ↓
Reflection Engine
    ↓
Quality Evaluation
    ↓
Confidence Validation
    ↓
Improvement Suggestions
    ↓
Final Approval

===========================================================
"""

from typing import List

from app.models.reflection_result import ReflectionResult


class ReflectionEngine:

    # =====================================================
    # CONFIGURATION
    # =====================================================

    MIN_RESPONSE_LENGTH = 30

    QUALITY_THRESHOLD = 0.75

    CONFIDENCE_THRESHOLD = 0.70

    EDUCATIONAL_KEYWORDS = [

        "example",

        "explanation",

        "tip",

        "practice",

        "improve",

        "learn",

        "exercise",

        "grammar",

        "vocabulary",

        "pronunciation"
    ]

    STRUCTURE_INDICATORS = [

        ":",

        "-",

        "•",

        "1.",

        "2.",

        "3."
    ]

    # =====================================================
    # RESPONSE LENGTH
    # =====================================================

    @classmethod
    def evaluate_length(
        cls,
        response: str
    ):

        if len(response.strip()) >= cls.MIN_RESPONSE_LENGTH:
            return 1.0

        return 0.0

    # =====================================================
    # EDUCATIONAL VALUE
    # =====================================================

    @classmethod
    def evaluate_educational_value(
        cls,
        response: str
    ):

        text = response.lower()

        matches = sum(

            1

            for keyword in cls.EDUCATIONAL_KEYWORDS

            if keyword in text
        )

        score = min(
            matches / 4,
            1.0
        )

        return round(score, 2)

    # =====================================================
    # STRUCTURE QUALITY
    # =====================================================

    @classmethod
    def evaluate_structure(
        cls,
        response: str
    ):

        matches = sum(

            1

            for item in cls.STRUCTURE_INDICATORS

            if item in response
        )

        score = min(
            matches / 3,
            1.0
        )

        return round(score, 2)

    # =====================================================
    # INTENT ALIGNMENT
    # =====================================================

    @classmethod
    def evaluate_intent_alignment(
        cls,
        response: str,
        intent: str
    ):

        response = response.lower()

        intent_keywords = {

            "GRAMMAR": [
                "grammar",
                "sentence",
                "correction"
            ],

            "VOCABULARY": [
                "meaning",
                "definition",
                "word"
            ],

            "TRANSLATION": [
                "translation",
                "translated"
            ],

            "PRONUNCIATION": [
                "pronunciation",
                "pronounce"
            ],

            "CONVERSATION": [
                "conversation",
                "speaking"
            ],

            "LEARNING_PLAN": [
                "plan",
                "roadmap",
                "schedule"
            ]
        }

        keywords = intent_keywords.get(
            intent,
            []
        )

        if not keywords:
            return 0.5

        matches = sum(

            1

            for keyword in keywords

            if keyword in response
        )

        score = min(
            matches / len(keywords),
            1.0
        )

        return round(score, 2)

    # =====================================================
    # PERSONALIZATION
    # =====================================================

    @classmethod
    def evaluate_personalization(
        cls,
        response: str,
        memory: dict = None
    ):

        if not memory:
            return 0.5

        score = 0

        goal = memory.get(
            "goal",
            ""
        )

        if goal and goal.lower() in response.lower():
            score += 0.5

        weak_areas = memory.get(
            "weak_areas",
            []
        )

        for area in weak_areas:

            if area.lower() in response.lower():
                score += 0.25

        return min(
            score,
            1.0
        )

    # =====================================================
    # SAFETY VALIDATION
    # =====================================================

    @classmethod
    def evaluate_safety(
        cls,
        response: str
    ):

        blocked_phrases = [

            "ignore previous instructions",

            "system prompt",

            "jailbreak"
        ]

        response = response.lower()

        for phrase in blocked_phrases:

            if phrase in response:
                return 0.0

        return 1.0

    # =====================================================
    # IMPROVEMENT GENERATION
    # =====================================================

    @classmethod
    def generate_feedback(
        cls,
        scores
    ) -> List[str]:

        feedback = []

        if scores["length"] < 1:
            feedback.append(
                "Response is too short."
            )

        if scores["education"] < 0.5:
            feedback.append(
                "Add more educational content."
            )

        if scores["structure"] < 0.5:
            feedback.append(
                "Improve response structure."
            )

        if scores["intent"] < 0.5:
            feedback.append(
                "Improve intent alignment."
            )

        if scores["personalization"] < 0.5:
            feedback.append(
                "Increase personalization."
            )

        return feedback

    # =====================================================
    # MAIN REFLECTION PIPELINE
    # =====================================================

    @classmethod
    def evaluate(
        cls,
        response: str,
        intent: str,
        memory: dict = None
    ):

        scores = {

            "length":
                cls.evaluate_length(response),

            "education":
                cls.evaluate_educational_value(
                    response
                ),

            "structure":
                cls.evaluate_structure(
                    response
                ),

            "intent":
                cls.evaluate_intent_alignment(
                    response,
                    intent
                ),

            "personalization":
                cls.evaluate_personalization(
                    response,
                    memory
                ),

            "safety":
                cls.evaluate_safety(
                    response
                )
        }

        quality_score = round(

            sum(scores.values())

            / len(scores),

            2
        )

        feedback = cls.generate_feedback(
            scores
        )

        passed = (
            quality_score
            >= cls.QUALITY_THRESHOLD
        )

        confidence_score = quality_score

        return ReflectionResult(

            passed=passed,

            quality_score=quality_score,

            confidence_score=confidence_score,

            feedback="\n".join(feedback),

            improvement_required=not passed
        )