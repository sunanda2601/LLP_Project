"""
LLP - CULTURAL BRIDGE AGENT

Purpose:
- Detect mother-tongue influenced English
- Detect literal translations
- Handle Telugu-English, Hinglish and Tanglish
- Rewrite into globally professional English
- Preserve the user's intended meaning
- Return a fixed JSON-compatible structure

Model:
- Ministral 3 8B via Ollama
"""

import json
import os
import re
from typing import Any, Dict

import ollama


class CulturalBridgeAgent:

    MODEL_NAME = os.getenv(
        "CULTURAL_BRIDGE_MODEL",
        "ministral-3:8b"
    )

    SYSTEM_PROMPT = """
You are the Cultural Bridge Agent for the LLP
(Language Learning Pal) application.

Your job is to detect genuine mother-tongue influenced
English and improve it into natural, professional English.

Pay attention to:

1. Telugu-English
2. Hinglish
3. Tanglish
4. Literal translations from Indian languages
5. Unnatural regional phrasing

IMPORTANT RULES:

- Preserve the user's intended meaning.
- Do not add information that is not present.
- Do not remove important meaning.
- Do not criticize the user's culture or language.
- Do not assume Indian English is incorrect.
- Only identify a cultural or literal-language issue
  when there is a genuine issue.
- If the sentence is already professional English,
  keep the improved sentence unchanged.
- Keep the explanation short and learner-friendly.

Return ONLY valid JSON.

Required JSON format:

{
    "issue": "description of the issue",
    "original": "original user sentence",
    "improved": "improved professional English sentence",
    "reason": "short explanation"
}

Do not use Markdown.
Do not add text before the JSON.
Do not add text after the JSON.
"""

    @classmethod
    def _extract_json(
        cls,
        text: str
    ) -> Dict[str, Any]:

        if not text:
            raise ValueError(
                "Empty response from Cultural Bridge Agent"
            )

        text = text.strip()

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

        try:
            result = json.loads(text)

            if isinstance(result, dict):
                return result

        except json.JSONDecodeError:
            pass

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

    @classmethod
    def _validate_result(
        cls,
        result: Dict[str, Any],
        original: str
    ) -> Dict[str, str]:

        required_fields = [
            "issue",
            "original",
            "improved",
            "reason"
        ]

        for field in required_fields:

            if field not in result:
                result[field] = ""

        return {
            "issue": str(
                result.get("issue", "")
            ).strip(),

            "original": original,

            "improved": str(
                result.get("improved") or original
            ).strip(),

            "reason": str(
                result.get("reason", "")
            ).strip()
        }

    @classmethod
    def process(
        cls,
        text: str
    ) -> Dict[str, str]:

        if not text or not text.strip():

            return {
                "issue": "Invalid input",
                "original": text or "",
                "improved": "",
                "reason": "Input cannot be empty."
            }

        original = text.strip()

        prompt = f"""
Analyze the following sentence using the Cultural Bridge rules.

User sentence:
{original}

Determine whether the sentence contains:

- Telugu-English influence
- Hinglish influence
- Tanglish influence
- Literal translation
- Unnatural regional phrasing
- Or no genuine cultural-language issue

If there is a genuine issue, rewrite the sentence into
natural, globally professional English.

If there is no genuine issue, keep the improved sentence
the same as the original.

Preserve the intended meaning.

Return ONLY the required JSON object.
"""

        try:

            response = ollama.chat(
                model=cls.MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": cls.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                format="json",
                options={
                    "temperature": 0.2,
                    "num_predict": 500
                }
            )

            content = response.message.content

            result = cls._extract_json(
                content
            )

            return cls._validate_result(
                result,
                original
            )

        except Exception as e:

            return {
                "issue": "Agent processing error",
                "original": original,
                "improved": original,
                "reason": str(e)
            }

    @classmethod
    def health_check(
        cls
    ) -> Dict[str, Any]:

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


if __name__ == "__main__":

    print("=" * 55)
    print("LLP Cultural Bridge Agent")
    print("=" * 55)

    print(
        "Model:",
        CulturalBridgeAgent.MODEL_NAME
    )

    print("\nHealth Check:")

    print(
        CulturalBridgeAgent.health_check()
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