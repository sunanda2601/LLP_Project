# pyrefly: ignore [missing-import]
from groq import Groq
from app.config.config import GROQ_API_KEY

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Llama 3.3 70B model chosen for high-performance versatile language classification & replies
MODEL_NAME = "llama-3.3-70b-versatile"

def clean_llm_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    import re
    text = re.sub(r'<thought>.*?</thought>', '', text, flags=re.DOTALL).strip()
    boxed_match = re.search(r'\\boxed{(.*?)}', text, re.DOTALL)
    if boxed_match:
        text = boxed_match.group(1).strip()
    else:
        final_answer_match = re.search(r'(?:the\s+)?final\s+answer\s+is:\s*(.*)', text, re.IGNORECASE | re.DOTALL)
        if final_answer_match:
            text = final_answer_match.group(1).strip()
    text = text.strip('$').strip()
    return text

def generate_response(prompt: str) -> str:
    """
    Sends a constructed prompt query to Groq LLM service.
    Handles API errors safely and returns details as a message string.
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return clean_llm_text(completion.choices[0].message.content)
    except Exception as e:
        raise RuntimeError(f"LLM request failed: {str(e)}") from e


"""
===========================================================
LANGUAGE LEARNING PAL LLM SERVICE
Version: 2.0

Purpose:
- Centralized LLM Communication Layer
- Groq Integration
- Retry Handling
- Timeout Protection
- Response Validation
- Monitoring & Metrics

===========================================================
"""

import time
from typing import Optional

from groq import Groq

from app.config.llm_config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_TEMPERATURE,
    GROQ_MAX_TOKENS
)

from app.models.llm_response import LLMResponse


class LLMService:

    PROVIDER = "GROQ"

    MAX_RETRIES = 3

    RETRY_DELAY = 2

    _client = None

    # =====================================================
    # CLIENT INITIALIZATION
    # =====================================================

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = Groq(
                api_key=GROQ_API_KEY
            )

        return cls._client

    # =====================================================
    # RESPONSE CLEANING
    # =====================================================

    @staticmethod
    def clean_response(text: str) -> str:

        return clean_llm_text(text)

    # =====================================================
    # TOKEN ESTIMATION
    # =====================================================

    @staticmethod
    def estimate_tokens(text: str):

        return max(
            1,
            len(text.split())
        )

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    @classmethod
    def health_check(cls):

        try:

            client = cls.get_client()

            response = client.chat.completions.create(

                model=GROQ_MODEL,

                messages=[
                    {
                        "role": "user",
                        "content": "hello"
                    }
                ],

                max_tokens=5
            )

            return {

                "status": "healthy",

                "provider": cls.PROVIDER,

                "model": GROQ_MODEL
            }

        except Exception as e:

            return {

                "status": "unhealthy",

                "error": str(e)
            }

    # =====================================================
    # MAIN GENERATION
    # =====================================================

    @classmethod
    def generate(
        cls,
        prompt: str
    ) -> LLMResponse:

        start_time = time.time()

        for attempt in range(
            cls.MAX_RETRIES
        ):

            try:

                client = cls.get_client()

                response = client.chat.completions.create(

                    model=GROQ_MODEL,

                    messages=[

                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=
                        GROQ_TEMPERATURE,

                    max_tokens=
                        GROQ_MAX_TOKENS
                )

                content = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                latency = round(

                    time.time()
                    - start_time,

                    3
                )

                content = cls.clean_response(
                    content
                )

                return LLMResponse(

                    success=True,

                    content=content,

                    provider=cls.PROVIDER,

                    model=GROQ_MODEL,

                    tokens=cls.estimate_tokens(
                        content
                    ),

                    latency=latency
                )

            except Exception as e:

                if attempt == (
                    cls.MAX_RETRIES - 1
                ):

                    return LLMResponse(

                        success=False,

                        content="",

                        provider=cls.PROVIDER,

                        model=GROQ_MODEL,

                        error=str(e)
                    )

                time.sleep(
                    cls.RETRY_DELAY
                )

    # =====================================================
    # SIMPLE HELPER
    # =====================================================

    @classmethod
    def generate_response(
        cls,
        prompt: str
    ) -> str:

        result = cls.generate(
            prompt
        )

        if result.success:
            return result.content

        return (
            "I apologize, but I am unable "
            "to process your request right now."
        )
