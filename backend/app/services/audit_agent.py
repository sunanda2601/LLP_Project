"""
===========================================================
LLP — AUDIT AGENT
Phase 2 — Sathwik

Purpose:
- Final QA pass on the merged pipeline output
- Check spelling, punctuation, capitalization
- Detect hallucinated corrections from upstream agents
- Return a fixed JSON-compatible structure

Receives input from:
- Grammar Agent
- Vocabulary Agent
- Cultural Bridge Agent
- Confidence Coach Agent

Output contract:
{
    "errors_found": [],
    "corrected_output": "...",
    "hallucination_flagged": false
}

Model:
- Configurable via AUDIT_AGENT_MODEL env var
- Default: ministral-3:8b (locally available)
- Intended: Ministral 3 3B when available
===========================================================
"""

import json
import os
import re
from typing import Any, Dict, List, Union

try:
    import ollama
except ImportError:
    ollama = None


# =========================================================
# AUDIT AGENT
# =========================================================

class AuditAgent:

    MODEL_NAME = os.getenv(
        "AUDIT_AGENT_MODEL",
        "ministral-3:8b"
    )

    # NOTE: The storyboard specifies Ministral 3 3B.
    # Set AUDIT_AGENT_MODEL=ministral-3:3b (or the exact
    # Ollama tag) in your environment when available.

    SYSTEM_PROMPT = """
You are the Audit Agent for the LLP (Language Learning Pal)
application.

Your job is to perform a final quality-assurance pass on
text that has already been processed by upstream agents
(Grammar, Vocabulary, Cultural Bridge, Confidence Coach).

You must check for:

1. SPELLING — identify and correct any remaining misspellings.
2. PUNCTUATION — identify and fix incorrect or missing
   punctuation (commas, periods, apostrophes, etc.).
3. CAPITALIZATION — fix improper capitalization (e.g.,
   sentences not starting with a capital letter, proper
   nouns not capitalized).
4. HALLUCINATION — detect if an upstream agent has
   ADDED information that was NOT in the original input,
   or has REPLACED a correct word/phrase with an incorrect
   one. Flag this as hallucination_flagged=true.

IMPORTANT RULES:

- Do NOT rewrite content that is already correct.
- Do NOT change technical terms, acronyms, or proper nouns
  unless they are genuinely misspelled.
- Do NOT add information that is not present.
- If no errors are found, return an empty errors_found list
  and set corrected_output to the original input unchanged.
- Be conservative: only flag something as a hallucination
  if there is clear evidence of fabricated content.

Return ONLY valid JSON. No Markdown. No extra text.

Required JSON format:

{
    "errors_found": [
        {
            "type": "spelling|punctuation|capitalization|hallucination",
            "original": "the incorrect fragment",
            "corrected": "the corrected version",
            "explanation": "brief reason"
        }
    ],
    "corrected_output": "the fully corrected text",
    "hallucination_flagged": false
}

If no errors are found, return:

{
    "errors_found": [],
    "corrected_output": "<original text unchanged>",
    "hallucination_flagged": false
}

Do not use Markdown code fences.
Do not add text before the JSON.
Do not add text after the JSON.
"""

    # =====================================================
    # PRIVATE: JSON EXTRACTION
    # =====================================================

    @classmethod
    def _extract_json(
        cls,
        text: str
    ) -> Dict[str, Any]:
        """
        Parse JSON from raw LLM output.

        Handles:
        - Clean JSON responses
        - Markdown code fences
        - Embedded JSON objects
        """

        if not text:
            raise ValueError(
                "Empty response from Audit Agent"
            )

        text = text.strip()

        # Strip markdown code fences
        text = re.sub(
            r"^```json\s*",
            "",
            text,
            flags=re.IGNORECASE
        )
        text = re.sub(r"^```\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

        # Attempt direct parse
        try:
            result = json.loads(text)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass

        # Fallback: extract first {...} block
        match = re.search(
            r"\{.*\}",
            text,
            flags=re.DOTALL
        )
        if match:
            try:
                result = json.loads(match.group(0))
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError:
                pass

        raise ValueError(
            "Audit Agent returned invalid JSON. "
            f"Raw output: {text[:200]}"
        )

    # =====================================================
    # PRIVATE: RESULT VALIDATION
    # =====================================================

    @classmethod
    def _validate_result(
        cls,
        result: Dict[str, Any],
        original: str
    ) -> Dict[str, Any]:
        """
        Enforce the output contract.

        - errors_found must be a list (default [])
        - corrected_output defaults to original if missing
        - hallucination_flagged must be bool
        """

        errors_found = result.get("errors_found", [])
        if not isinstance(errors_found, list):
            errors_found = []

        # Sanitise each error entry
        clean_errors: List[Dict[str, str]] = []
        for err in errors_found:
            if isinstance(err, dict):
                clean_errors.append({
                    "type": str(
                        err.get("type", "unknown")
                    ).strip(),
                    "original": str(
                        err.get("original", "")
                    ).strip(),
                    "corrected": str(
                        err.get("corrected", "")
                    ).strip(),
                    "explanation": str(
                        err.get("explanation", "")
                    ).strip(),
                })

        corrected_output = str(
            result.get("corrected_output") or original
        ).strip()

        raw_flag = result.get("hallucination_flagged", False)
        hallucination_flagged = bool(raw_flag)

        return {
            "errors_found": clean_errors,
            "corrected_output": corrected_output,
            "hallucination_flagged": hallucination_flagged,
        }

    # =====================================================
    # PRIVATE: EXTRACT TEXT FROM UPSTREAM
    # =====================================================

    @classmethod
    def _extract_text_from_upstream(
        cls,
        upstream: Union[str, Dict[str, Any]]
    ) -> str:
        """
        Extract a plain-text string from upstream agent output.

        Upstream may be:
        - A plain string
        - A dict with 'improved', 'response', or 'message' key
        - A malformed/None value
        """

        if upstream is None:
            return ""

        if isinstance(upstream, str):
            return upstream.strip()

        if isinstance(upstream, dict):
            # Try common output fields in priority order
            for key in ("improved", "response", "message", "corrected_output"):
                val = upstream.get(key)
                if val and isinstance(val, str):
                    return val.strip()

        # Last resort: stringify
        return str(upstream).strip()

    # =====================================================
    # PUBLIC: PROCESS
    # =====================================================

    @classmethod
    def process(
        cls,
        text: Union[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Run the final QA audit pass on text.

        Accepts either:
        - A plain string
        - A merged upstream dict (extracts text automatically)

        Always returns the required schema.
        Never raises — errors are returned as safe fallbacks.
        """

        # Extract text from upstream dict if needed
        extracted = cls._extract_text_from_upstream(text)

        # Guard: empty input
        if not extracted:
            return {
                "errors_found": [],
                "corrected_output": "",
                "hallucination_flagged": False,
            }

        original = extracted

        # Guard: missing dependency
        if ollama is None:
            return {
                "errors_found": [],
                "corrected_output": original,
                "hallucination_flagged": False,
            }

        user_prompt = f"""
Perform a final quality-assurance audit on the following text.

Text to audit:
{original}

Check for:
1. Spelling errors
2. Punctuation errors
3. Capitalization errors
4. Hallucinated or fabricated content not present in the input

If no issues are found, return an empty errors_found list
and set corrected_output to the original text unchanged.

Return ONLY the required JSON object.
"""

        try:
            response = ollama.chat(
                model=cls.MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": cls.SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                format="json",
                options={
                    "temperature": 0.1,
                    "num_predict": 200,
                },
            )

            content = response.message.content

            result = cls._extract_json(content)

            return cls._validate_result(result, original)

        except Exception as e:
            # Fail gracefully — never crash the pipeline
            return {
                "errors_found": [],
                "corrected_output": original,
                "hallucination_flagged": False,
                "_error": str(e),
            }

    # =====================================================
    # PUBLIC: HEALTH CHECK
    # =====================================================

    @classmethod
    def health_check(cls) -> Dict[str, Any]:

        if ollama is None:
            return {
                "status": "unhealthy",
                "provider": "ollama",
                "model": cls.MODEL_NAME,
                "error": (
                    "The 'ollama' Python package is not installed."
                ),
            }

        try:
            response = ollama.chat(
                model=cls.MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": "Return only the word OK.",
                    }
                ],
                options={
                    "temperature": 0,
                    "num_predict": 10,
                },
            )

            return {
                "status": "healthy",
                "provider": "ollama",
                "model": cls.MODEL_NAME,
                "response": response.message.content,
            }

        except Exception as e:

            return {
                "status": "unhealthy",
                "provider": "ollama",
                "model": cls.MODEL_NAME,
                "error": str(e),
            }


# =========================================================
# MODULE SELF-TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 55)
    print("LLP Audit Agent")
    print("=" * 55)

    print("Model:", AuditAgent.MODEL_NAME)

    print("\nHealth Check:")
    print(AuditAgent.health_check())

    test_cases = [
        ("spelling",      "The managment decicion was approvd."),
        ("punctuation",   "I went to the store but I forgot my wallet"),
        ("capitalization","the quick brown fox jumps over the lazy dog."),
        ("clean",         "The management decision was approved yesterday."),
    ]

    for label, text in test_cases:
        print(f"\n--- {label.upper()} ---")
        result = AuditAgent.process(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
