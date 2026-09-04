"""
===========================================================
LANGUAGE LEARNING PAL REFLECTION ENGINE TEST SUITE
Version: 2.0

Purpose:
- Quality Evaluation
- Safety Evaluation
- Confidence Evaluation
- Reflection Validation
- Feedback Validation

===========================================================
"""

import pytest

from app.services.reflection_engine import (
    ReflectionEngine
)


# =========================================================
# LENGTH EVALUATION
# =========================================================

def test_length_score_short():

    score = (
        ReflectionEngine
        .evaluate_length(
            "Hello"
        )
    )

    assert isinstance(
        score,
        float
    )


def test_length_score_medium():

    response = """
    Grammar Correction:

    I went to school yesterday.

    Explanation:
    Use the past tense of go.
    """

    score = (
        ReflectionEngine
        .evaluate_length(
            response
        )
    )

    assert score >= 0


def test_length_score_large():

    response = (
        "English learning content "
        * 300
    )

    score = (
        ReflectionEngine
        .evaluate_length(
            response
        )
    )

    assert score >= 0


# =========================================================
# SAFETY EVALUATION
# =========================================================

def test_safe_response():

    score = (
        ReflectionEngine
        .evaluate_safety(
            "This is a safe educational response."
        )
    )

    assert score == 1.0


def test_empty_response_safety():

    score = (
        ReflectionEngine
        .evaluate_safety("")
    )

    assert score >= 0


# =========================================================
# EDUCATIONAL QUALITY
# =========================================================

def test_grammar_quality():

    response = """
    Grammar Correction:

    Original:
    I goed to school.

    Correct:
    I went to school.

    Explanation:
    The past tense of go is went.
    """

    result = (
        ReflectionEngine.evaluate(

            response=response,

            intent="GRAMMAR"
        )
    )

    assert result is not None


def test_translation_quality():

    response = """
    Translation:

    Hello → నమస్తే

    Usage:
    Common greeting.
    """

    result = (
        ReflectionEngine.evaluate(

            response=response,

            intent="TRANSLATION"
        )
    )

    assert result is not None


# =========================================================
# CONFIDENCE VALIDATION
# =========================================================

def test_confidence_score_exists():

    result = (
        ReflectionEngine.evaluate(

            response="""
            Vocabulary:

            Perseverance means
            continued effort.
            """,

            intent="VOCABULARY"
        )
    )

    assert hasattr(
        result,
        "confidence_score"
    )


# =========================================================
# QUALITY SCORE VALIDATION
# =========================================================

def test_quality_score_exists():

    result = (
        ReflectionEngine.evaluate(

            response="""
            Grammar Correction:

            I went to school.
            """,

            intent="GRAMMAR"
        )
    )

    assert hasattr(
        result,
        "quality_score"
    )


# =========================================================
# PASSED FLAG
# =========================================================

def test_reflection_passed_flag():

    result = (
        ReflectionEngine.evaluate(

            response="""
            Translation:

            Hello → నమస్తే
            """,

            intent="TRANSLATION"
        )
    )

    assert hasattr(
        result,
        "passed"
    )


# =========================================================
# FEEDBACK VALIDATION
# =========================================================

def test_feedback_exists():

    result = (
        ReflectionEngine.evaluate(

            response="""
            Vocabulary:

            Resilient means
            recovering quickly.
            """,

            intent="VOCABULARY"
        )
    )

    assert hasattr(
        result,
        "feedback"
    )


# =========================================================
# EMPTY RESPONSE
# =========================================================

def test_empty_response():

    result = (
        ReflectionEngine.evaluate(

            response="",

            intent="GRAMMAR"
        )
    )

    assert result is not None


# =========================================================
# UNICODE RESPONSE
# =========================================================

def test_unicode_response():

    result = (
        ReflectionEngine.evaluate(

            response="నమస్తే",

            intent="TRANSLATION"
        )
    )

    assert result is not None


# =========================================================
# LONG RESPONSE
# =========================================================

def test_large_response():

    response = (
        "English learning content "
        * 500
    )

    result = (
        ReflectionEngine.evaluate(

            response=response,

            intent="VOCABULARY"
        )
    )

    assert result is not None


# =========================================================
# MULTIPLE INTENTS
# =========================================================

@pytest.mark.parametrize(

    "intent",

    [

        "GRAMMAR",

        "VOCABULARY",

        "TRANSLATION",

        "PRONUNCIATION",

        "CONVERSATION",

        "LEARNING_PLAN"
    ]
)
def test_supported_intents(intent):

    result = (
        ReflectionEngine.evaluate(

            response="""
            Sample educational response.
            """,

            intent=intent
        )
    )

    assert result is not None


# =========================================================
# CONSISTENCY
# =========================================================

def test_consistent_reflection():

    response = """
    Grammar Correction:

    I went to school.
    """

    result1 = (
        ReflectionEngine.evaluate(

            response=response,

            intent="GRAMMAR"
        )
    )

    result2 = (
        ReflectionEngine.evaluate(

            response=response,

            intent="GRAMMAR"
        )
    )

    assert (
        result1.passed
        ==
        result2.passed
    )


# =========================================================
# PERFORMANCE
# =========================================================

def test_bulk_reflections():

    results = []

    for _ in range(25):

        result = (
            ReflectionEngine.evaluate(

                response="""
                Vocabulary:
                Perseverance means
                continued effort.
                """,

                intent="VOCABULARY"
            )
        )

        results.append(result)

    assert len(results) == 25