"""
=============================================================
LLP - CULTURAL BRIDGE AGENT
=============================================================

Purpose:
- Detect mother-tongue influenced English
- Detect literal translations
- Handle Telugu-English, Hinglish and Tanglish
- Rewrite into globally professional English
- Preserve the user's intended meaning
- Return a fixed JSON-compatible structure

Model:
- Ministral 3 8B via Ollama

Prompt:
- Loaded from app.prompts.cultural_bridge_prompt
=============================================================
"""

import json
import os
import re
from typing import Any, Dict

try:
    import ollama
except ImportError:
    ollama = None


# =============================================================
# CULTURAL BRIDGE PROMPT
# =============================================================

from app.prompts.cultural_bridge_prompts import (
    CULTURAL_BRIDGE_SYSTEM_PROMPT,
    build_cultural_bridge_prompt,
)


class CulturalBridgeAgent:
    """
    Cultural Bridge Agent.

    Detects genuine first-language influence and regional
    phrasing and rewrites it into natural professional English.
    """

    # =========================================================
    # MODEL CONFIGURATION
    # =========================================================

    MODEL_NAME = os.getenv(
        "CULTURAL_BRIDGE_MODEL",
        "ministral-3:8b"
    )

    # Keep SYSTEM_PROMPT as an alias for backward compatibility
    # with any existing code that may reference it.
    SYSTEM_PROMPT = CULTURAL_BRIDGE_SYSTEM_PROMPT

    # =========================================================
    # JSON EXTRACTION
    # =========================================================

    @classmethod
    def _extract_json(
        cls,
        text: str
    ) -> Dict[str, Any]:
        """
        Extract a JSON object from the model response.

        Handles:
        - Pure JSON
        - JSON surrounded by whitespace
        - Markdown code fences
        - Extra text surrounding a JSON object
        """

        if not text:
            raise ValueError(
                "Empty response from Cultural Bridge Agent"
            )

        text = text.strip()

        # -----------------------------------------------------
        # Remove Markdown JSON code fence
        # -----------------------------------------------------

        text = re.sub(
            r"^```json\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"^```\s*",
            "",
            text
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        text = text.strip()

        # -----------------------------------------------------
        # Try direct JSON parsing first
        # -----------------------------------------------------

        try:
            result = json.loads(text)

            if isinstance(result, dict):
                return result

        except json.JSONDecodeError:
            pass

        # -----------------------------------------------------
        # Try extracting JSON object from surrounding text
        # -----------------------------------------------------

        match = re.search(
            r"\{.*\}",
            text,
            flags=re.DOTALL
        )

        if match:

            try:
                result = json.loads(
                    match.group(0)
                )

                if isinstance(result, dict):
                    return result

            except json.JSONDecodeError:
                pass

        raise ValueError(
            "Cultural Bridge Agent returned invalid JSON"
        )

    # =========================================================
    # RESULT VALIDATION
    # =========================================================

    @classmethod
    def _validate_result(
        cls,
        result: Dict[str, Any],
        original: str
    ) -> Dict[str, str]:
        """
        Validate and normalize the Cultural Bridge output.

        Required fields:

        issue
        original
        improved
        reason
        """

        required_fields = [
            "issue",
            "original",
            "improved",
            "reason"
        ]

        # -----------------------------------------------------
        # Ensure all required fields exist
        # -----------------------------------------------------

        for field in required_fields:

            if field not in result:
                result[field] = ""

        # -----------------------------------------------------
        # Normalize values
        # -----------------------------------------------------

        issue = str(
            result.get("issue", "")
        ).strip()

        improved = str(
            result.get("improved") or original
        ).strip()

        reason = str(
            result.get("reason", "")
        ).strip()

        # -----------------------------------------------------
        # If model returned empty improved text,
        # preserve original.
        # -----------------------------------------------------

        if not improved:
            improved = original

        # -----------------------------------------------------
        # Return fixed schema
        # -----------------------------------------------------

        return {
            "issue": issue,
            "original": original,
            "improved": improved,
            "reason": reason
        }

    # =========================================================
    # MAIN PROCESS METHOD
    # =========================================================

    @classmethod
    def process(
        cls,
        text: str
    ) -> Dict[str, str]:
        """
        Process a user sentence through the Cultural Bridge Agent.

        Returns:

        {
            "issue": "...",
            "original": "...",
            "improved": "...",
            "reason": "..."
        }
        """

        # -----------------------------------------------------
        # Validate input
        # -----------------------------------------------------

        if not text or not text.strip():

            return {
                "issue": "Invalid input",
                "original": text or "",
                "improved": "",
                "reason": "Input cannot be empty."
            }

        original = text.strip()

        # -----------------------------------------------------
        # Check Ollama dependency
        # -----------------------------------------------------

        if ollama is None:

            return {
                "issue": "Agent dependency missing",
                "original": original,
                "improved": original,
                "reason": (
                    "The 'ollama' Python package is not installed."
                )
            }

        # -----------------------------------------------------
        # Build prompt from centralized prompt module
        # -----------------------------------------------------

        prompt = build_cultural_bridge_prompt(
            original
        )

        # -----------------------------------------------------
        # Ollama inference
        # -----------------------------------------------------

        try:

            response = ollama.chat(
                model=cls.MODEL_NAME,

                messages=[
                    {
                        "role": "system",
                        "content": CULTURAL_BRIDGE_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                # Request structured JSON
                format="json",

                options={
                    "temperature": 0.2,
                    "num_predict": 250
                }
            )

            # -------------------------------------------------
            # Extract model content
            # -------------------------------------------------

            content = response.message.content

            # -------------------------------------------------
            # Parse JSON
            # -------------------------------------------------

            result = cls._extract_json(
                content
            )

            # -------------------------------------------------
            # Validate fixed schema
            # -------------------------------------------------

            return cls._validate_result(
                result,
                original
            )

        except Exception as e:

            # -------------------------------------------------
            # Fail safely
            # -------------------------------------------------

            return {
                "issue": "Agent processing error",
                "original": original,
                "improved": original,
                "reason": str(e)
            }

    # =========================================================
    # HEALTH CHECK
    # =========================================================

    @classmethod
    def health_check(
        cls
    ) -> Dict[str, Any]:
        """
        Verify that Ollama and the configured model are available.
        """

        # -----------------------------------------------------
        # Check Python Ollama package
        # -----------------------------------------------------

        if ollama is None:

            return {
                "status": "unhealthy",
                "provider": "ollama",
                "model": cls.MODEL_NAME,
                "error": (
                    "The 'ollama' Python package is not installed."
                )
            }

        # -----------------------------------------------------
        # Test Ollama model
        # -----------------------------------------------------

        try:

            response = ollama.chat(
                model=cls.MODEL_NAME,

                messages=[
                    {
                        "role": "user",
                        "content": "Return only the word OK."
                    }
                ],

                options={
                    "temperature": 0,
                    "num_predict": 10
                }
            )

            return {
                "status": "healthy",
                "provider": "ollama",
                "model": cls.MODEL_NAME,
                "response": response.message.content
            }

        except Exception as e:

            return {
                "status": "unhealthy",
                "provider": "ollama",
                "model": cls.MODEL_NAME,
                "error": str(e)
            }


# =============================================================
# DIRECT TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("LLP Cultural Bridge Agent")
    print("=" * 60)

    print(
        "Model:",
        CulturalBridgeAgent.MODEL_NAME
    )

    print("\nHealth Check:")

    print(
        json.dumps(
            CulturalBridgeAgent.health_check(),
            indent=2,
            ensure_ascii=False
        )
    )

    print("\nSample Test:")

    sample = (
        "I am having a doubt regarding this project."
    )

    result = CulturalBridgeAgent.process(
        sample
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )