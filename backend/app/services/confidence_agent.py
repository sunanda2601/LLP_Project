"""
===========================================================
LLP — CONFIDENCE COACH AGENT
Phase 1 — Sathwik

Purpose:
- Detect passive, apologetic, hesitant, aggressive, or
  already-confident tone in user text
- Rewrite into calibrated, confident, professional language
- Preserve the user's intended meaning
- Do NOT over-assert; preserve legitimate uncertainty
- Return a fixed JSON-compatible structure

Output contract:
{
    "tone_detected": "passive|apologetic|hesitant|aggressive|confident",
    "original": "<original user text>",
    "improved": "<rewritten text>",
    "reason": "<short explanation>"
}

Model:
- Configurable via CONFIDENCE_COACH_MODEL env var
- Default: ministral-3:8b (locally available)
- Intended: Ministral 3 14B when available
===========================================================
"""

import json
import os
import re
from typing import Any, Dict

try:
    import ollama
except ImportError:
    ollama = None


# =========================================================
# VALID TONE CATEGORIES
# =========================================================

VALID_TONES = {
    "passive",
    "apologetic",
    "hesitant",
    "aggressive",
    "confident",
}


# =========================================================
# CONFIDENCE COACH AGENT
# =========================================================

class ConfidenceAgent:

    MODEL_NAME = os.getenv(
        "CONFIDENCE_COACH_MODEL",
        "ministral-3:8b"
    )

    # NOTE: The storyboard specifies Ministral 3 14B.
    # Set CONFIDENCE_COACH_MODEL=ministral-3:14b (or the
    # exact Ollama tag) in your environment when available.

    SYSTEM_PROMPT = """
You are the Confidence Coach for the LLP (Language Learning Pal)
application.

Your job is to analyze the user's text, detect the dominant
tone, and rewrite it into calibrated, confident, professional
language when necessary.

TONE CATEGORIES you must distinguish:

1. passive — indirect constructions, avoids ownership, e.g.:
   "It might be considered that this approach could be improved."
   → "This approach can be improved."

2. apologetic — unnecessary apologies or over-qualifications:
   "Sorry, I think maybe this could possibly work?"
   → "This should work."

3. hesitant — excessive hedging that weakens a valid point:
   "I'm not sure, but perhaps we could consider trying this."
   → "I recommend trying this approach."

4. aggressive — overly forceful, confrontational, or dismissive:
   "You need to fix this immediately. This is completely wrong."
   → "Please address this — the current approach has an issue."

5. confident — already well-calibrated, professional language:
   "I recommend proceeding with this approach."
   → No rewrite needed. Keep the improved text identical.

IMPORTANT RULES:

- Detect the SINGLE dominant tone.
- Preserve the user's intended meaning exactly.
- Do NOT add information that is not present.
- Do NOT remove important meaning.
- Do NOT turn professional language into aggressive language.
- Do NOT over-assert. If the user is expressing genuine
  uncertainty ("I'm not sure whether X or Y"), preserve that.
- Do NOT rewrite already-confident sentences unnecessarily.
- Remove unnecessary apologies ("sorry", "I apologize") when
  they do not serve a genuine purpose.
- Remove hedging words ("maybe", "perhaps", "possibly",
  "I think", "I feel like") when they weaken a valid claim.
- Keep hedging when uncertainty is factually appropriate.
- Use clear, direct, professional English.
- Do NOT hallucinate facts or invent context.

Return ONLY valid JSON. No Markdown. No extra text.

Required JSON format:

{
    "tone_detected": "passive|apologetic|hesitant|aggressive|confident",
    "original": "original user text",
    "improved": "rewritten confident professional text",
    "reason": "brief explanation of the change"
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
        - Markdown code fences (```json ... ```)
        - Embedded JSON objects in surrounding text
        """

        if not text:
            raise ValueError(
                "Empty response from Confidence Coach"
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
            "Confidence Coach returned invalid JSON. "
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
    ) -> Dict[str, str]:
        """
        Enforce the output contract.

        - Normalise tone_detected to a known category.
        - Ensure original is preserved from the input.
        - Ensure improved defaults to original when missing.
        - Ensure reason is always a string.
        """

        # Normalise tone
        raw_tone = str(
            result.get("tone_detected", "")
        ).strip().lower()

        # Accept partial matches for robustness
        tone = "confident"  # safe default
        for valid in VALID_TONES:
            if valid in raw_tone:
                tone = valid
                break

        improved = str(
            result.get("improved") or original
        ).strip()

        reason = str(
            result.get("reason", "")
        ).strip()

        return {
            "tone_detected": tone,
            "original": original,
            "improved": improved,
            "reason": reason,
        }

    # =====================================================
    # PUBLIC: PROCESS
    # =====================================================

    @classmethod
    def process(
        cls,
        text: str
    ) -> Dict[str, str]:
        """
        Analyse text tone and return a calibrated rewrite.

        Always returns the required schema.
        Never raises — errors are returned as safe fallbacks.
        """

        # Guard: empty / whitespace input
        if not text or not text.strip():
            return {
                "tone_detected": "confident",
                "original": text or "",
                "improved": "",
                "reason": "Input is empty or whitespace.",
            }

        original = text.strip()

        # Guard: missing dependency
        if ollama is None:
            return {
                "tone_detected": "confident",
                "original": original,
                "improved": original,
                "reason": (
                    "The 'ollama' Python package is not installed."
                ),
            }

        user_prompt = f"""
Analyze the following text using the Confidence Coach rules.

Text:
{original}

Identify the dominant tone from:
passive, apologetic, hesitant, aggressive, confident

If the tone needs improvement, rewrite it into calibrated,
confident, professional language while preserving the meaning.

If the text is already confident and professional, set
"improved" to the original text and explain that no change
was needed.

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
                    "temperature": 0.2,
                    "num_predict": 200,
                },
            )

            content = response.message.content

            result = cls._extract_json(content)

            return cls._validate_result(result, original)

        except Exception as e:
            # Fail gracefully — never crash the pipeline
            return {
                "tone_detected": "confident",
                "original": original,
                "improved": original,
                "reason": (
                    f"Agent processing error: {str(e)}"
                ),
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
    print("LLP Confidence Coach Agent")
    print("=" * 55)

    print("Model:", ConfidenceAgent.MODEL_NAME)

    print("\nHealth Check:")
    print(ConfidenceAgent.health_check())

    test_cases = [
        ("passive",     "I think this approach could maybe be improved."),
        ("apologetic",  "Sorry, I think maybe this could possibly work?"),
        ("hesitant",    "I'm not sure, but perhaps we could consider trying this."),
        ("aggressive",  "You need to fix this immediately. This is completely wrong."),
        ("confident",   "I recommend proceeding with this approach."),
    ]

    for label, text in test_cases:
        print(f"\n--- {label.upper()} ---")
        result = ConfidenceAgent.process(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
