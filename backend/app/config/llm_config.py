"""
===========================================================
LANGUAGE LEARNING PAL LLM CONFIGURATION
Version: 2.0

Purpose:
- Centralized LLM Configuration
- Model Management
- Provider Configuration
- Generation Settings
- Timeout & Retry Policies

Supported Providers:
- Groq
- OpenAI (Future)
- Gemini (Future)

===========================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BACKEND_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=BACKEND_ROOT / ".env", override=False)

# =========================================================
# ACTIVE PROVIDER
# =========================================================

LLM_PROVIDER = "GROQ"

# =========================================================
# GROQ CONFIGURATION
# =========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.3-70b-versatile"

GROQ_TEMPERATURE = 0.3

GROQ_MAX_TOKENS = 4000

GROQ_TOP_P = 1.0

GROQ_TIMEOUT = 30

# =========================================================
# RETRY CONFIGURATION
# =========================================================

MAX_RETRIES = 3

RETRY_DELAY_SECONDS = 2

# =========================================================
# RESPONSE CONFIGURATION
# =========================================================

MIN_RESPONSE_LENGTH = 10

MAX_RESPONSE_LENGTH = 5000

ENABLE_RESPONSE_CLEANING = True

ENABLE_RESPONSE_VALIDATION = True

# =========================================================
# SAFETY CONFIGURATION
# =========================================================

ENABLE_SAFETY_CHECKS = True

ENABLE_REFLECTION_ENGINE = True

ENABLE_GUARDRAILS = True

# =========================================================
# PERFORMANCE CONFIGURATION
# =========================================================

ENABLE_METRICS = True

ENABLE_LATENCY_TRACKING = True

ENABLE_TOKEN_ESTIMATION = True

# =========================================================
# PROMPT CONFIGURATION
# =========================================================

PROMPT_VERSION = "2.0"

MAX_PROMPT_LENGTH = 12000

# =========================================================
# FALLBACK RESPONSES
# =========================================================

DEFAULT_ERROR_MESSAGE = (
    "I apologize, but I am unable to process "
    "your request right now. Please try again."
)

DEFAULT_TIMEOUT_MESSAGE = (
    "The request is taking longer than expected. "
    "Please try again shortly."
)

DEFAULT_OUT_OF_DOMAIN_MESSAGE = (
    "I specialize in language learning and "
    "communication-related assistance."
)

# =========================================================
# HEALTH CHECK CONFIGURATION
# =========================================================

HEALTH_CHECK_PROMPT = "Hello"

HEALTH_CHECK_MAX_TOKENS = 5

# =========================================================
# AGENT CONFIGURATION
# =========================================================

ENABLE_MEMORY_CONTEXT = True

ENABLE_TOOL_CONTEXT = True

ENABLE_REFLECTION_CONTEXT = True

ENABLE_PERSONALIZATION = True

# =========================================================
# DEBUG CONFIGURATION
# =========================================================

DEBUG_MODE = False

LOG_PROMPTS = False

LOG_RESPONSES = False