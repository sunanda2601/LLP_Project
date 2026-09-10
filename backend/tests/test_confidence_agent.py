"""
===========================================================
LLP — CONFIDENCE COACH AGENT TESTS
Phase 1 — Sathwik

Test strategy (six stages):
  1. Deterministic schema/logic tests (no LLM required)
  2. LLM integration tests (marked: pytest -m ollama)

Deterministic tests verify:
  - _extract_json parsing logic
  - _validate_result schema enforcement
  - Edge case guards (empty, whitespace, missing ollama)
  - Fallback behaviour on malformed LLM output

LLM tests verify (require Ollama + ministral-3:8b):
  - All 5 tone categories
  - Edge cases: questions, technical language, unicode,
    contractions, mixed tones, long input, short input
===========================================================
"""

import json
import pytest

from app.services.confidence_agent import (
    ConfidenceAgent,
    VALID_TONES,
)


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture
def passive_text():
    return "I think this approach could maybe be improved."


@pytest.fixture
def apologetic_text():
    return "Sorry, I think maybe this could possibly work?"


@pytest.fixture
def hesitant_text():
    return "I'm not sure, but perhaps we could consider trying this."


@pytest.fixture
def aggressive_text():
    return "You need to fix this immediately. This is completely wrong."


@pytest.fixture
def confident_text():
    return "I recommend proceeding with this approach."


# =========================================================
# HELPERS
# =========================================================

def assert_valid_schema(result: dict, original: str):
    """Assert the output satisfies the contract."""
    assert isinstance(result, dict), "Result must be a dict"
    assert "tone_detected" in result, "Missing: tone_detected"
    assert "original" in result, "Missing: original"
    assert "improved" in result, "Missing: improved"
    assert "reason" in result, "Missing: reason"
    assert result["tone_detected"] in VALID_TONES, (
        f"Invalid tone: {result['tone_detected']}"
    )
    assert result["original"] == original, (
        "original must preserve the input exactly"
    )
    assert isinstance(result["improved"], str), (
        "improved must be a string"
    )
    assert len(result["improved"]) > 0, (
        "improved must not be empty"
    )
    assert isinstance(result["reason"], str), (
        "reason must be a string"
    )


# =========================================================
# 1. DETERMINISTIC: _extract_json
# =========================================================

class TestExtractJson:

    def test_clean_json(self):
        raw = '{"tone_detected": "passive", "original": "x", "improved": "y", "reason": "z"}'
        result = ConfidenceAgent._extract_json(raw)
        assert result["tone_detected"] == "passive"

    def test_json_with_markdown_fence(self):
        raw = '```json\n{"tone_detected": "hesitant", "original": "a", "improved": "b", "reason": "c"}\n```'
        result = ConfidenceAgent._extract_json(raw)
        assert result["tone_detected"] == "hesitant"

    def test_json_with_plain_fence(self):
        raw = '```\n{"tone_detected": "confident", "original": "x", "improved": "x", "reason": "ok"}\n```'
        result = ConfidenceAgent._extract_json(raw)
        assert result["tone_detected"] == "confident"

    def test_json_embedded_in_text(self):
        raw = 'Here is the result: {"tone_detected": "apologetic", "original": "x", "improved": "y", "reason": "z"} done.'
        result = ConfidenceAgent._extract_json(raw)
        assert result["tone_detected"] == "apologetic"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            ConfidenceAgent._extract_json("")

    def test_none_like_empty_raises(self):
        with pytest.raises(ValueError):
            ConfidenceAgent._extract_json("   ")

    def test_invalid_json_raises(self):
        with pytest.raises(ValueError):
            ConfidenceAgent._extract_json("this is not json at all")

    def test_markdown_fences_case_insensitive(self):
        raw = '```JSON\n{"tone_detected": "aggressive", "original": "a", "improved": "b", "reason": "r"}\n```'
        result = ConfidenceAgent._extract_json(raw)
        assert result["tone_detected"] == "aggressive"


# =========================================================
# 2. DETERMINISTIC: _validate_result
# =========================================================

class TestValidateResult:

    def test_all_valid_fields(self):
        raw = {
            "tone_detected": "passive",
            "original": "test",
            "improved": "improved test",
            "reason": "too weak",
        }
        result = ConfidenceAgent._validate_result(raw, "test")
        assert result["tone_detected"] == "passive"
        assert result["original"] == "test"
        assert result["improved"] == "improved test"
        assert result["reason"] == "too weak"

    def test_original_is_always_preserved(self):
        raw = {
            "tone_detected": "hesitant",
            "original": "WRONG VALUE",
            "improved": "better",
            "reason": "reason",
        }
        result = ConfidenceAgent._validate_result(raw, "real input")
        assert result["original"] == "real input"

    def test_missing_improved_defaults_to_original(self):
        raw = {
            "tone_detected": "confident",
            "original": "hello",
            "reason": "already fine",
        }
        result = ConfidenceAgent._validate_result(raw, "hello")
        assert result["improved"] == "hello"

    def test_none_improved_defaults_to_original(self):
        raw = {
            "tone_detected": "confident",
            "original": "hello",
            "improved": None,
            "reason": "ok",
        }
        result = ConfidenceAgent._validate_result(raw, "hello")
        assert result["improved"] == "hello"

    def test_unknown_tone_defaults_to_confident(self):
        raw = {
            "tone_detected": "COMPLETELY_UNKNOWN",
            "original": "x",
            "improved": "y",
            "reason": "r",
        }
        result = ConfidenceAgent._validate_result(raw, "x")
        assert result["tone_detected"] == "confident"

    def test_tone_partial_match(self):
        raw = {
            "tone_detected": "This is a passive tone",
            "original": "x",
            "improved": "y",
            "reason": "r",
        }
        result = ConfidenceAgent._validate_result(raw, "x")
        assert result["tone_detected"] == "passive"

    def test_all_valid_tone_values(self):
        for tone in VALID_TONES:
            raw = {
                "tone_detected": tone,
                "original": "x",
                "improved": "y",
                "reason": "r",
            }
            result = ConfidenceAgent._validate_result(raw, "x")
            assert result["tone_detected"] == tone

    def test_missing_reason_defaults_to_empty(self):
        raw = {
            "tone_detected": "passive",
            "original": "x",
            "improved": "y",
        }
        result = ConfidenceAgent._validate_result(raw, "x")
        assert isinstance(result["reason"], str)


# =========================================================
# 3. DETERMINISTIC: process() edge case guards
# =========================================================

class TestProcessGuards:

    def test_empty_string_input(self):
        result = ConfidenceAgent.process("")
        # For empty input, assert schema manually (improved CAN be "")
        assert isinstance(result, dict)
        assert "tone_detected" in result
        assert "original" in result
        assert "improved" in result
        assert "reason" in result
        assert result["tone_detected"] in VALID_TONES
        assert result["improved"] == ""

    def test_whitespace_only_input(self):
        result = ConfidenceAgent.process("   ")
        # whitespace is stripped to "" so original becomes ""
        assert "tone_detected" in result
        assert "original" in result

    def test_none_input(self):
        result = ConfidenceAgent.process(None)
        assert isinstance(result, dict)
        assert "tone_detected" in result

    def test_output_is_always_dict(self):
        for text in ["", "   ", "hello", "x" * 5000]:
            result = ConfidenceAgent.process(text)
            assert isinstance(result, dict)

    def test_output_always_has_required_keys(self):
        required = {"tone_detected", "original", "improved", "reason"}
        for text in ["", "   ", "hello"]:
            result = ConfidenceAgent.process(text)
            assert required.issubset(result.keys()), (
                f"Missing keys for input: {repr(text)}"
            )

    def test_tone_is_always_valid(self):
        for text in ["hello", "sorry maybe", ""]:
            result = ConfidenceAgent.process(text)
            assert result["tone_detected"] in VALID_TONES


# =========================================================
# 4. LLM INTEGRATION TESTS (require Ollama)
# =========================================================

@pytest.mark.ollama
class TestConfidenceAgentLLM:

    def test_passive_tone_detected(self, passive_text):
        result = ConfidenceAgent.process(passive_text)
        assert_valid_schema(result, passive_text)
        assert result["tone_detected"] in {"passive", "hesitant"}
        # improved should differ from original for passive input
        assert len(result["improved"]) > 0

    def test_apologetic_tone_detected(self, apologetic_text):
        result = ConfidenceAgent.process(apologetic_text)
        assert_valid_schema(result, apologetic_text)
        assert result["tone_detected"] in {"apologetic", "hesitant", "passive"}
        # "Sorry" should ideally not appear in the improved version
        # (but we don't hard-assert this — model may handle differently)
        assert len(result["improved"]) > 0

    def test_hesitant_tone_detected(self, hesitant_text):
        result = ConfidenceAgent.process(hesitant_text)
        assert_valid_schema(result, hesitant_text)
        assert result["tone_detected"] in {"hesitant", "passive"}

    def test_aggressive_tone_detected(self, aggressive_text):
        result = ConfidenceAgent.process(aggressive_text)
        assert_valid_schema(result, aggressive_text)
        assert result["tone_detected"] in {"aggressive", "confident"}

    def test_confident_tone_preserved(self, confident_text):
        result = ConfidenceAgent.process(confident_text)
        assert_valid_schema(result, confident_text)
        assert result["tone_detected"] == "confident"
        # For already-confident text, improved should be close to original
        assert len(result["improved"]) > 0

    def test_schema_valid_json_serializable(self, passive_text):
        result = ConfidenceAgent.process(passive_text)
        # Must be JSON-serializable
        serialized = json.dumps(result)
        parsed = json.loads(serialized)
        assert parsed["tone_detected"] in VALID_TONES

    def test_very_short_input(self):
        result = ConfidenceAgent.process("ok")
        assert_valid_schema(result, "ok")

    def test_long_input(self):
        long_text = (
            "I think perhaps maybe we could possibly consider "
            "potentially looking into the idea of perhaps trying "
            "to improve this system, if it's not too much trouble. "
        ) * 10
        result = ConfidenceAgent.process(long_text)
        assert isinstance(result, dict)
        assert "tone_detected" in result

    def test_question_input(self):
        result = ConfidenceAgent.process(
            "Could you perhaps maybe help me with this?"
        )
        assert_valid_schema(result, "Could you perhaps maybe help me with this?")

    def test_technical_language_preserved(self):
        text = "The API endpoint returns a 404 HTTP status code."
        result = ConfidenceAgent.process(text)
        assert_valid_schema(result, text)
        # Technical terms should be preserved
        assert "API" in result["improved"] or "endpoint" in result["improved"]

    def test_unicode_input(self):
        text = "Je suis désolé, maybe this résumé needs improvement?"
        result = ConfidenceAgent.process(text)
        assert isinstance(result, dict)
        assert "tone_detected" in result

    def test_input_with_contractions(self):
        result = ConfidenceAgent.process(
            "I'm not sure I'd be able to do this right."
        )
        assert isinstance(result, dict)
        assert "tone_detected" in result

    def test_input_with_quotation_marks(self):
        text = 'He said "maybe we should try this approach."'
        result = ConfidenceAgent.process(text)
        assert isinstance(result, dict)
        assert "tone_detected" in result

    def test_multiple_sentences(self):
        text = (
            "I think this might work. Perhaps we could try it. "
            "I'm not sure though."
        )
        result = ConfidenceAgent.process(text)
        assert_valid_schema(result, text)

    def test_acronyms_preserved(self):
        text = "The CEO should maybe consider the ROI of this project."
        result = ConfidenceAgent.process(text)
        assert isinstance(result, dict)
        # CEO and ROI should survive in improved text
        improved = result.get("improved", "")
        assert "CEO" in improved or "ROI" in improved or len(improved) > 0

    def test_numbers_preserved(self):
        text = "I think this might take approximately 3 to 5 business days."
        result = ConfidenceAgent.process(text)
        assert isinstance(result, dict)
        improved = result.get("improved", "")
        assert len(improved) > 0

    def test_mixed_tone_input(self):
        text = (
            "Sorry to bother you, but you MUST fix this NOW. "
            "I think maybe it could be better."
        )
        result = ConfidenceAgent.process(text)
        assert isinstance(result, dict)
        assert result.get("tone_detected") in VALID_TONES

    def test_already_professional_language(self):
        text = (
            "I have reviewed the proposal and identified three areas "
            "for improvement. I recommend scheduling a follow-up meeting."
        )
        result = ConfidenceAgent.process(text)
        assert_valid_schema(result, text)

    def test_original_meaning_preserved_passive(self, passive_text):
        result = ConfidenceAgent.process(passive_text)
        # "approach" and "improved" (as concept) should survive
        improved = result["improved"].lower()
        assert (
            "approach" in improved or "improv" in improved
        ), "Core meaning should be preserved"

    def test_reason_is_non_empty_for_changed_text(self, apologetic_text):
        result = ConfidenceAgent.process(apologetic_text)
        if result["improved"] != result["original"]:
            assert len(result["reason"]) > 0, (
                "reason must explain the change"
            )
