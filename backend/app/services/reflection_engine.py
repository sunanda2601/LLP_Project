"""
===========================================================
LANGUAGE LEARNING PAL REFLECTION ENGINE
Version: 2.2

Purpose:
- Self Evaluation
- Response Validation
- Quality Assessment
- Confidence Scoring
- Improvement Suggestions
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
        "pronunciation",
        "rule",
        "correct"
    ]

    STRUCTURE_INDICATORS = [

        # Grammar
        "Original:",
        "Corrected:",
        "Explanation:",
        "Grammar Rule:",
        "Natural Version:",
        "Grammar Tip:",

        # Vocabulary
        "Word:",
        "Meaning:",
        "Part of Speech:",
        "Example:",
        "Synonyms:",
        "Antonyms:",
        "Actionable Tip:",

        # Translation
        "Translation:",
        "English:",
        "Telugu:",

        # General
        "Practice:",
        "Tip:"
    ]

    # =====================================================
    # RESPONSE LENGTH
    # =====================================================

    @classmethod
    def evaluate_length(cls, response: str):

        if not response:
            return 0.0

        if len(response.strip()) >= cls.MIN_RESPONSE_LENGTH:
            return 1.0

        return 0.0

    # =====================================================
    # EDUCATIONAL VALUE
    # =====================================================

    @classmethod
    def evaluate_educational_value(cls, response: str):

        if not response:
            return 0.0

        text = response.lower()

        matches = sum(
            1
            for keyword in cls.EDUCATIONAL_KEYWORDS
            if keyword.lower() in text
        )

        score = min(matches / 4, 1.0)

        return round(score, 2)

    # =====================================================
    # STRUCTURE QUALITY
    # =====================================================

    @classmethod
    def evaluate_structure(cls, response: str):

        if not response:
            return 0.0

        matches = sum(
            1
            for indicator in cls.STRUCTURE_INDICATORS
            if indicator.lower() in response.lower()
        )

        score = min(matches / 4, 1.0)

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

        if not response:
            return 0.0

        response_lower = response.lower().strip()

        # -------------------------------------------------
        # TRANSLATION
        # -------------------------------------------------
        # Translation responses may contain only the target
        # language. Therefore, English keywords such as
        # "translation" should not be required.
        # A non-empty translation is considered aligned.
        # -------------------------------------------------

        if intent == "TRANSLATION":

            if response_lower:
                return 1.0

            return 0.0

        # -------------------------------------------------
        # OTHER INTENTS
        # -------------------------------------------------

        intent_keywords = {

            "GRAMMAR": [
                "correct",
                "grammar",
                "sentence",
                "explanation",
                "grammar rule"
            ],

            "VOCABULARY": [
                "meaning",
                "definition",
                "word"
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

        keywords = intent_keywords.get(intent, [])

        if not keywords:
            return 0.5

        matches = sum(
            1
            for keyword in keywords
            if keyword in response_lower
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

        # No memory means personalization is not applicable.
        # Do not penalize the response.
        if not memory:
            return 1.0

        profile = memory.get(
            "profile",
            memory
        )

        goal = profile.get(
            "goal",
            ""
        )

        weak_areas = profile.get(
            "weak_areas",
            []
        )

        score = 0.0

        if goal and goal.lower() in response.lower():
            score += 0.5

        for area in weak_areas:

            if area.lower() in response.lower():
                score += 0.25

        # If memory exists but contains no personalization
        # requirements, do not penalize.
        if not goal and not weak_areas:
            return 1.0

        return min(
            score,
            1.0
        )

    # =====================================================
    # SAFETY VALIDATION
    # =====================================================

    @classmethod
    def evaluate_safety(cls, response: str):

        if not response:
            return 0.0

        blocked_phrases = [
            "ignore previous instructions",
            "system prompt",
            "jailbreak"
        ]

        response_lower = response.lower()

        for phrase in blocked_phrases:

            if phrase in response_lower:
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

        if scores["safety"] < 1:
            feedback.append(
                "Response failed safety validation."
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

        # -------------------------------------------------
        # Calculate normal scores
        # -------------------------------------------------

        scores = {

            "length":
                cls.evaluate_length(response),

            "education":
                cls.evaluate_educational_value(response),

            "structure":
                cls.evaluate_structure(response),

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
                cls.evaluate_safety(response)
        }

        # -------------------------------------------------
        # Translation-specific scoring
        # -------------------------------------------------
        # A translation can be a short target-language
        # sentence and does not need educational labels.
        # Therefore, do not penalize translation responses
        # for length, education, or English structure.
        # -------------------------------------------------

        if intent == "TRANSLATION":

            scores["length"] = 1.0
            scores["education"] = 1.0
            scores["structure"] = 1.0

        # -------------------------------------------------
        # Intent-aware weighting
        # -------------------------------------------------

        if intent == "GRAMMAR":

            weights = {

                "length": 0.10,
                "education": 0.20,
                "structure": 0.20,
                "intent": 0.25,
                "personalization": 0.05,
                "safety": 0.20
            }

        elif intent == "TRANSLATION":

            weights = {

                "length": 0.05,
                "education": 0.05,
                "structure": 0.10,
                "intent": 0.30,
                "personalization": 0.10,
                "safety": 0.40
            }

        else:

            weights = {

                "length": 0.15,
                "education": 0.20,
                "structure": 0.20,
                "intent": 0.20,
                "personalization": 0.10,
                "safety": 0.15
            }

        # -------------------------------------------------
        # Calculate quality score
        # -------------------------------------------------

        quality_score = round(

            sum(
                scores[key] * weights[key]
                for key in scores
            ),

            2
        )

        # -------------------------------------------------
        # Generate feedback
        # -------------------------------------------------

        feedback = cls.generate_feedback(
            scores
        )

        # -------------------------------------------------
        # Pass / Fail
        # -------------------------------------------------

        passed = (
            quality_score
            >= cls.QUALITY_THRESHOLD
        )

        confidence_score = quality_score

        # -------------------------------------------------
        # Return reflection result
        # -------------------------------------------------

        return ReflectionResult(

            passed=passed,

            quality_score=quality_score,

            confidence_score=confidence_score,

            feedback="\n".join(feedback),

            improvement_required=not passed
        )