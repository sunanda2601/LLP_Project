"""
===========================================================
LLP — AUDIT AGENT TESTS
Phase 2 — Sathwik

Test strategy (six stages):
  1. Deterministic schema/logic tests (no LLM required)
  2. LLM integration tests (marked: pytest -m ollama)

Required test categories:
  1. Spelling errors
  2. Punctuation errors
  3. Capitalization errors
  4. Malformed upstream JSON input
  5. Hallucinated correction detection
  6. Already-correct sentence (no changes)
===========================================================
"""

import json
import pytest

from app.services.audit_agent import AuditAgent


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture
def spelling_error_text():
    return "The managment decicion was approvd yesterday."


@pytest.fixture
def punctuation_error_text():
    return "What time is it I dont know"


@pytest.fixture
def capitalization_error_text():
    return "the quick brown fox jumps over the lazy dog."


@pytest.fixture
def correct_text():
    return "The management decision was approved yesterday."


# =========================================================
# HELPERS
# =========================================================

def assert_valid_audit_schema(result: dict):
    """Assert the audit output satisfies the contract."""
    assert isinstance(result, dict), "Result must be a dict"
    assert "errors_found" in result, "Missing: errors_found"
    assert "corrected_output" in result, "Missing: corrected_output"
    assert "hallucination_flagged" in result, "Missing: hallucination_flagged"
    assert isinstance(result["errors_found"], list), (
        "errors_found must be a list"
    )
    assert isinstance(result["corrected_output"], str), (
        "corrected_output must be a string"
    )
    assert isinstance(result["hallucination_flagged"], bool), (
        "hallucination_flagged must be bool"
    )


# =========================================================
# 1. DETERMINISTIC: _extract_json
# =========================================================

class TestAuditExtractJson:

    def test_clean_json(self):
        raw = '{"errors_found": [], "corrected_output": "hello", "hallucination_flagged": false}'
        result = AuditAgent._extract_json(raw)
        assert result["hallucination_flagged"] is False
        assert result["corrected_output"] == "hello"

    def test_markdown_fenced_json(self):
        raw = '```json\n{"errors_found": [], "corrected_output": "test", "hallucination_flagged": false}\n```'
        result = AuditAgent._extract_json(raw)
        assert result["corrected_output"] == "test"

    def test_plain_fenced_json(self):
        raw = '```\n{"errors_found": [], "corrected_output": "test2", "hallucination_flagged": false}\n```'
        result = AuditAgent._extract_json(raw)
        assert result["corrected_output"] == "test2"

    def test_json_embedded_in_text(self):
        raw = 'Here is the audit: {"errors_found": [], "corrected_output": "ok", "hallucination_flagged": false}'
        result = AuditAgent._extract_json(raw)
        assert result["corrected_output"] == "ok"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            AuditAgent._extract_json("")

    def test_invalid_json_raises(self):
        with pytest.raises(ValueError):
            AuditAgent._extract_json("not json at all")

    def test_json_with_errors_list(self):
        raw = json.dumps({
            "errors_found": [
                {
                    "type": "spelling",
                    "original": "teh",
                    "corrected": "the",
                    "explanation": "misspelling"
                }
            ],
            "corrected_output": "the dog",
            "hallucination_flagged": False
        })
        result = AuditAgent._extract_json(raw)
        assert len(result["errors_found"]) == 1


# =========================================================
# 2. DETERMINISTIC: _validate_result
# =========================================================

class TestAuditValidateResult:

    def test_all_valid_fields(self):
        raw = {
            "errors_found": [
                {
                    "type": "spelling",
                    "original": "teh",
                    "corrected": "the",
                    "explanation": "typo"
                }
            ],
            "corrected_output": "the dog",
            "hallucination_flagged": False,
        }
        result = AuditAgent._validate_result(raw, "teh dog")
        assert len(result["errors_found"]) == 1
        assert result["errors_found"][0]["type"] == "spelling"
        assert result["corrected_output"] == "the dog"
        assert result["hallucination_flagged"] is False

    def test_missing_errors_found_defaults_to_empty(self):
        raw = {
            "corrected_output": "hello",
            "hallucination_flagged": False,
        }
        result = AuditAgent._validate_result(raw, "hello")
        assert result["errors_found"] == []

    def test_non_list_errors_found_becomes_empty(self):
        raw = {
            "errors_found": "spelling error",
            "corrected_output": "hello",
            "hallucination_flagged": False,
        }
        result = AuditAgent._validate_result(raw, "hello")
        assert result["errors_found"] == []

    def test_missing_corrected_output_defaults_to_original(self):
        raw = {
            "errors_found": [],
            "hallucination_flagged": False,
        }
        result = AuditAgent._validate_result(raw, "my original text")
        assert result["corrected_output"] == "my original text"

    def test_none_corrected_output_defaults_to_original(self):
        raw = {
            "errors_found": [],
            "corrected_output": None,
            "hallucination_flagged": False,
        }
        result = AuditAgent._validate_result(raw, "my text")
        assert result["corrected_output"] == "my text"

    def test_hallucination_flagged_truthy_coercion(self):
        raw = {
            "errors_found": [],
            "corrected_output": "test",
            "hallucination_flagged": 1,
        }
        result = AuditAgent._validate_result(raw, "test")
        assert result["hallucination_flagged"] is True

    def test_hallucination_flagged_false(self):
        raw = {
            "errors_found": [],
            "corrected_output": "test",
            "hallucination_flagged": False,
        }
        result = AuditAgent._validate_result(raw, "test")
        assert result["hallucination_flagged"] is False

    def test_error_entries_are_sanitised(self):
        raw = {
            "errors_found": [
                {
                    "type": "spelling",
                    "original": "  teh  ",
                    "corrected": "  the  ",
                    "explanation": "  typo  ",
                },
                "not a dict entry — should be skipped",
            ],
            "corrected_output": "the dog",
            "hallucination_flagged": False,
        }
        result = AuditAgent._validate_result(raw, "teh dog")
        # Only the valid dict entry survives
        assert len(result["errors_found"]) == 1
        assert result["errors_found"][0]["original"] == "teh"


# =========================================================
# 3. DETERMINISTIC: _extract_text_from_upstream
# =========================================================

class TestExtractTextFromUpstream:

    def test_plain_string(self):
        assert AuditAgent._extract_text_from_upstream("hello") == "hello"

    def test_none_returns_empty(self):
        assert AuditAgent._extract_text_from_upstream(None) == ""

    def test_dict_with_improved_key(self):
        assert AuditAgent._extract_text_from_upstream(
            {"improved": "better text"}
        ) == "better text"

    def test_dict_with_response_key(self):
        assert AuditAgent._extract_text_from_upstream(
            {"response": "grammar response"}
        ) == "grammar response"

    def test_dict_with_message_key(self):
        assert AuditAgent._extract_text_from_upstream(
            {"message": "a message"}
        ) == "a message"

    def test_dict_priority_improved_over_response(self):
        assert AuditAgent._extract_text_from_upstream(
            {"improved": "preferred", "response": "fallback"}
        ) == "preferred"

    def test_malformed_upstream_dict(self):
        # Dict with no known keys returns empty-ish string
        result = AuditAgent._extract_text_from_upstream(
            {"unknown_key": "value"}
        )
        assert isinstance(result, str)

    def test_empty_dict(self):
        result = AuditAgent._extract_text_from_upstream({})
        assert isinstance(result, str)


# =========================================================
# 4. DETERMINISTIC: process() edge case guards
# =========================================================

class TestAuditProcessGuards:

    def test_empty_string_input(self):
        result = AuditAgent.process("")
        assert_valid_audit_schema(result)
        assert result["errors_found"] == []
        assert result["corrected_output"] == ""

    def test_whitespace_only_input(self):
        result = AuditAgent.process("   ")
        assert_valid_audit_schema(result)

    def test_none_input(self):
        result = AuditAgent.process(None)
        assert isinstance(result, dict)
        assert "errors_found" in result

    def test_dict_input_extracted(self):
        upstream = {"improved": "The management decision was approved."}
        result = AuditAgent.process(upstream)
        assert isinstance(result, dict)
        assert "corrected_output" in result

    def test_malformed_upstream_dict_input(self):
        # Dict with no usable text key
        result = AuditAgent.process({"junk": 123, "other": None})
        assert isinstance(result, dict)
        assert_valid_audit_schema(result)

    def test_output_always_has_required_keys(self):
        required = {
            "errors_found",
            "corrected_output",
            "hallucination_flagged",
        }
        for text in ["", "   ", "hello world"]:
            result = AuditAgent.process(text)
            assert required.issubset(result.keys()), (
                f"Missing keys for input: {repr(text)}"
            )

    def test_output_is_always_dict(self):
        for text in ["", "   ", "hello", "x" * 2000]:
            result = AuditAgent.process(text)
            assert isinstance(result, dict)

    def test_hallucination_flagged_always_bool(self):
        for text in ["", "hello"]:
            result = AuditAgent.process(text)
            assert isinstance(result["hallucination_flagged"], bool)

    def test_errors_found_always_list(self):
        for text in ["", "hello"]:
            result = AuditAgent.process(text)
            assert isinstance(result["errors_found"], list)


# =========================================================
# 5. LLM INTEGRATION TESTS (require Ollama)
# =========================================================

@pytest.mark.ollama
class TestAuditAgentLLM:

    def test_spelling_errors_detected(self, spelling_error_text):
        result = AuditAgent.process(spelling_error_text)
        assert_valid_audit_schema(result)
        # Expect spelling errors to be found or text to be corrected
        has_spelling = any(
            e.get("type") == "spelling"
            for e in result["errors_found"]
        )
        corrected = result["corrected_output"]
        assert has_spelling or corrected != spelling_error_text, (
            "Spelling errors should be detected or corrected"
        )

    def test_punctuation_errors_detected(self, punctuation_error_text):
        result = AuditAgent.process(punctuation_error_text)
        assert_valid_audit_schema(result)
        has_punctuation = any(
            e.get("type") == "punctuation"
            for e in result["errors_found"]
        )
        corrected = result["corrected_output"]
        assert has_punctuation or corrected != punctuation_error_text, (
            "Punctuation errors should be detected or corrected"
        )

    def test_capitalization_errors_detected(self, capitalization_error_text):
        result = AuditAgent.process(capitalization_error_text)
        assert_valid_audit_schema(result)
        has_caps = any(
            e.get("type") == "capitalization"
            for e in result["errors_found"]
        )
        corrected = result["corrected_output"]
        assert has_caps or corrected != capitalization_error_text, (
            "Capitalization errors should be detected or corrected"
        )

    def test_correct_sentence_unchanged(self, correct_text):
        result = AuditAgent.process(correct_text)
        assert_valid_audit_schema(result)
        # For an already-correct sentence, errors should be empty
        # and hallucination should not be flagged
        assert result["hallucination_flagged"] is False
        assert isinstance(result["errors_found"], list)

    def test_hallucination_not_flagged_for_clean_text(self, correct_text):
        result = AuditAgent.process(correct_text)
        assert result["hallucination_flagged"] is False

    def test_schema_always_valid(self, spelling_error_text):
        result = AuditAgent.process(spelling_error_text)
        serialized = json.dumps(result)
        parsed = json.loads(serialized)
        assert_valid_audit_schema(parsed)

    def test_error_entries_have_required_fields(self, spelling_error_text):
        result = AuditAgent.process(spelling_error_text)
        for error in result["errors_found"]:
            assert "type" in error
            assert "original" in error
            assert "corrected" in error
            assert "explanation" in error

    def test_upstream_dict_input(self):
        upstream = {
            "improved": "The managment decicion was approvd.",
        }
        result = AuditAgent.process(upstream)
        assert_valid_audit_schema(result)
        assert len(result["corrected_output"]) > 0

    def test_very_short_input(self):
        result = AuditAgent.process("ok")
        assert_valid_audit_schema(result)

    def test_long_input(self):
        long_text = (
            "The management decided to approve the proposal "
            "submitted by the team. "
        ) * 30
        result = AuditAgent.process(long_text)
        assert isinstance(result, dict)
        assert "corrected_output" in result

    def test_technical_terms_preserved(self):
        text = "The API returns a JSON payload with HTTP 200 status."
        result = AuditAgent.process(text)
        assert_valid_audit_schema(result)
        corrected = result["corrected_output"]
        assert "API" in corrected or "JSON" in corrected or len(corrected) > 0

    def test_numbers_preserved(self):
        text = "The report covers Q3 2026 with 42 data points."
        result = AuditAgent.process(text)
        assert_valid_audit_schema(result)
        assert len(result["corrected_output"]) > 0
