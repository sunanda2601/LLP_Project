"""
Language Learning Pal - Local Ollama LLM Service
"""

import time
import requests

from app.models.llm_response import LLMResponse


# =========================================================
# OLLAMA CONFIGURATION
# =========================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "mistral:7b"

TEMPERATURE = 0.3
MAX_TOKENS = 4000
TIMEOUT = 120


# =========================================================
# RESPONSE CLEANING
# =========================================================

def clean_llm_text(text: str) -> str:
    if not text:
        return ""

    text = text.strip()

    import re

    text = re.sub(
        r"<thought>.*?</thought>",
        "",
        text,
        flags=re.DOTALL
    ).strip()

    boxed_match = re.search(
        r"\\boxed\{(.*?)\}",
        text,
        re.DOTALL
    )

    if boxed_match:
        text = boxed_match.group(1).strip()

    else:
        final_answer_match = re.search(
            r"(?:the\s+)?final\s+answer\s+is:\s*(.*)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if final_answer_match:
            text = final_answer_match.group(1).strip()

    return text.strip("$").strip()


# =========================================================
# OLLAMA GENERATION
# =========================================================

def generate_response(prompt: str) -> str:

    try:

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": TEMPERATURE,
                "num_predict": MAX_TOKENS
            }
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        content = data.get("response", "")

        return clean_llm_text(content)

    except Exception as e:

        raise RuntimeError(
            f"Ollama LLM request failed: {str(e)}"
        ) from e


# =========================================================
# LLM SERVICE CLASS
# =========================================================

class LLMService:

    PROVIDER = "OLLAMA"

    MAX_RETRIES = 3

    RETRY_DELAY = 2

    # -----------------------------------------------------
    # HEALTH CHECK
    # -----------------------------------------------------

    @classmethod
    def health_check(cls):

        try:

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": "Say hello",
                    "stream": False,
                    "options": {
                        "num_predict": 5
                    }
                },
                timeout=TIMEOUT
            )

            response.raise_for_status()

            return {
                "status": "healthy",
                "provider": cls.PROVIDER,
                "model": MODEL_NAME
            }

        except Exception as e:

            return {
                "status": "unhealthy",
                "provider": cls.PROVIDER,
                "model": MODEL_NAME,
                "error": str(e)
            }

    # -----------------------------------------------------
    # GENERATE
    # -----------------------------------------------------

    @classmethod
    def generate(cls, prompt: str) -> LLMResponse:

        start_time = time.time()

        for attempt in range(cls.MAX_RETRIES):

            try:

                content = generate_response(prompt)

                latency = round(
                    time.time() - start_time,
                    3
                )

                return LLMResponse(
                    success=True,
                    content=content,
                    provider=cls.PROVIDER,
                    model=MODEL_NAME,
                    tokens=max(1, len(content.split())),
                    tokens_used=max(1, len(content.split())),
                    latency=latency
                )

            except Exception as e:

                if attempt == cls.MAX_RETRIES - 1:

                    return LLMResponse(
                        success=False,
                        content="",
                        provider=cls.PROVIDER,
                        model=MODEL_NAME,
                        error=str(e),
                        latency=round(
                            time.time() - start_time,
                            3
                        )
                    )

                time.sleep(cls.RETRY_DELAY)

    # -----------------------------------------------------
    # SIMPLE HELPER
    # -----------------------------------------------------

    @classmethod
    def generate_response(cls, prompt: str) -> str:

        result = cls.generate(prompt)

        if result.success:
            return result.content

        return (
            "I apologize, but I am unable "
            "to process your request right now."
        )

    # -----------------------------------------------------
    # CLEAN RESPONSE
    # -----------------------------------------------------

    @staticmethod
    def clean_response(text: str) -> str:

        return clean_llm_text(text)

    # -----------------------------------------------------
    # TOKEN ESTIMATION
    # -----------------------------------------------------

    @staticmethod
    def estimate_tokens(text: str):

        return max(
            1,
            len(text.split())
        )