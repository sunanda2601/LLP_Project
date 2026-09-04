"""
===========================================================
LANGUAGE LEARNING PAL GUARDRAILS ENGINE
Version: 2.0

Responsibilities:
- Input Validation
- Prompt Injection Detection
- Jailbreak Detection
- Domain Validation
- Request Protection

This module is the first execution layer of the AI Agent.

Pipeline:

User Request
      ↓
Input Validation
      ↓
Prompt Injection Detection
      ↓
Jailbreak Detection
      ↓
Domain Validation
      ↓
Intent Engine

===========================================================
"""

import re

from app.config.agent_rules import (
    MAX_INPUT_LENGTH,
    MIN_INPUT_LENGTH,
    BLOCKED_PHRASES
)

from app.config.domain_config import (
    OUT_OF_DOMAIN_TOPICS
)

from app.config.error_codes import ErrorCode


class Guardrails:

    @staticmethod
    def validate_input(message: str):
        """
        Validate user input.
        """

        if message is None:
            return False, ErrorCode.EMPTY_INPUT

        if not message.strip():
            return False, ErrorCode.EMPTY_INPUT

        if len(message.strip()) < MIN_INPUT_LENGTH:
            return False, ErrorCode.INPUT_TOO_SHORT

        if len(message) > MAX_INPUT_LENGTH:
            return False, ErrorCode.INPUT_TOO_LONG

        return True, None

    @staticmethod
    def detect_prompt_injection(message: str):
        """
        Detect prompt injection attempts.
        """

        text = message.lower()

        for phrase in BLOCKED_PHRASES:
            if phrase.lower() in text:
                return False, ErrorCode.PROMPT_INJECTION_DETECTED

        return True, None

    @staticmethod
    def detect_jailbreak(message: str):
        """
        Detect jailbreak attempts.
        """

        jailbreak_patterns = [

            r"ignore.*instructions",

            r"ignore.*rules",

            r"forget.*rules",

            r"act as.*",

            r"bypass.*",

            r"developer mode",

            r"system prompt",

            r"jailbreak",

            r"override.*",

            r"disable.*safety",

            r"reveal.*prompt"
        ]

        text = message.lower()

        for pattern in jailbreak_patterns:

            if re.search(pattern, text):
                return False, ErrorCode.JAILBREAK_ATTEMPT_DETECTED

        return True, None

    @staticmethod
    def domain_check(message: str):
        """
        Detect out-of-domain requests.
        """

        text = message.lower()

        for topic in OUT_OF_DOMAIN_TOPICS:

            if topic.lower() in text:
                return False, ErrorCode.OUT_OF_DOMAIN_REQUEST

        return True, None

    @staticmethod
    def validate_request(message: str):
        """
        Run complete validation pipeline.

        Returns:
            (True, None)
            OR
            (False, ErrorCode)
        """

        validation_pipeline = [

            ("Input Validation",
             Guardrails.validate_input),

            ("Prompt Injection Detection",
             Guardrails.detect_prompt_injection),

            ("Jailbreak Detection",
             Guardrails.detect_jailbreak),

            ("Domain Validation",
             Guardrails.domain_check)
        ]

        for validation_name, validator in validation_pipeline:

            valid, error = validator(message)

            if not valid:
                print(
                    f"[GUARDRAILS FAILED] "
                    f"{validation_name} -> {error}"
                )

                return False, error

        return True, None