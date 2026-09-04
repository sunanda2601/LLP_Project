"""
===========================================================
LANGUAGE LEARNING PAL AGENT ERROR TAXONOMY
Version: 2.0

Purpose:
- Standardized error handling
- Agent observability
- Failure recovery
- Security monitoring
- Production-grade diagnostics

Every error should be:
1. Actionable
2. Traceable
3. Recoverable (when possible)
4. User-friendly

===========================================================
"""

from enum import Enum


class ErrorCode(str, Enum):

    # =====================================================
    # 1000 SERIES - INPUT VALIDATION
    # =====================================================

    EMPTY_INPUT = "LLA_1001"

    INPUT_TOO_SHORT = "LLA_1002"

    INPUT_TOO_LONG = "LLA_1003"

    INVALID_INPUT_FORMAT = "LLA_1004"

    UNSUPPORTED_CHARACTER_SET = "LLA_1005"

    # =====================================================
    # 2000 SERIES - DOMAIN VALIDATION
    # =====================================================

    OUT_OF_DOMAIN_REQUEST = "LLA_2001"

    UNSUPPORTED_LANGUAGE = "LLA_2002"

    UNSUPPORTED_INTENT = "LLA_2003"

    INVALID_GOAL = "LLA_2004"

    # =====================================================
    # 3000 SERIES - SECURITY
    # =====================================================

    PROMPT_INJECTION_DETECTED = "LLA_3001"

    JAILBREAK_ATTEMPT_DETECTED = "LLA_3002"

    SYSTEM_PROMPT_DISCLOSURE_ATTEMPT = "LLA_3003"

    ROLE_OVERRIDE_ATTEMPT = "LLA_3004"

    SECURITY_POLICY_VIOLATION = "LLA_3005"

    # =====================================================
    # 4000 SERIES - CLASSIFICATION ENGINE
    # =====================================================

    INTENT_CLASSIFICATION_FAILED = "LLA_4001"

    LOW_CONFIDENCE_CLASSIFICATION = "LLA_4002"

    ENTITY_EXTRACTION_FAILED = "LLA_4003"

    TASK_DECOMPOSITION_FAILED = "LLA_4004"

    # =====================================================
    # 5000 SERIES - MEMORY ENGINE
    # =====================================================

    MEMORY_RETRIEVAL_FAILED = "LLA_5001"

    MEMORY_UPDATE_FAILED = "LLA_5002"

    MEMORY_CORRUPTED = "LLA_5003"

    MEMORY_NOT_FOUND = "LLA_5004"

    MEMORY_LIMIT_EXCEEDED = "LLA_5005"

    # =====================================================
    # 6000 SERIES - PLANNING ENGINE
    # =====================================================

    PLAN_GENERATION_FAILED = "LLA_6001"

    PLAN_VALIDATION_FAILED = "LLA_6002"

    GOAL_ANALYSIS_FAILED = "LLA_6003"

    REASONING_FAILURE = "LLA_6004"

    # =====================================================
    # 7000 SERIES - TOOL LAYER
    # =====================================================

    TOOL_NOT_FOUND = "LLA_7001"

    TOOL_SELECTION_FAILED = "LLA_7002"

    TOOL_EXECUTION_FAILED = "LLA_7003"

    TOOL_TIMEOUT = "LLA_7004"

    EXTERNAL_API_FAILURE = "LLA_7005"

    TOOL_RESPONSE_INVALID = "LLA_7006"

    # =====================================================
    # 8000 SERIES - LLM LAYER
    # =====================================================

    LLM_CONNECTION_FAILED = "LLA_8001"

    LLM_TIMEOUT = "LLA_8002"

    LLM_RESPONSE_FAILED = "LLA_8003"

    LLM_RATE_LIMIT_EXCEEDED = "LLA_8004"

    LLM_INVALID_RESPONSE = "LLA_8005"

    # =====================================================
    # 9000 SERIES - RESPONSE ENGINE
    # =====================================================

    RESPONSE_GENERATION_FAILED = "LLA_9001"

    RESPONSE_VALIDATION_FAILED = "LLA_9002"

    RESPONSE_FORMATTING_FAILED = "LLA_9003"

    QUALITY_THRESHOLD_NOT_MET = "LLA_9004"

    # =====================================================
    # 10000 SERIES - SYSTEM
    # =====================================================

    CONFIGURATION_ERROR = "LLA_10001"

    DATABASE_CONNECTION_FAILED = "LLA_10002"

    SERVICE_UNAVAILABLE = "LLA_10003"

    INTERNAL_SERVER_ERROR = "LLA_10004"

    UNKNOWN_ERROR = "LLA_10005"