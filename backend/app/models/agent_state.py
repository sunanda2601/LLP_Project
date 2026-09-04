"""
===========================================================
LANGUAGE LEARNING PAL AGENT STATE MACHINE
Version: 2.0

Enterprise-grade lifecycle management for the
Language Learning Pal Agent.

Purpose:
- Track every stage of agent execution
- Improve observability and debugging
- Enable frontend status visualization
- Support planning, memory, tools, and reflection
- Provide auditability for evaluation and testing

===========================================================
"""

from enum import Enum


class AgentState(str, Enum):

    # ======================================================
    # INITIALIZATION
    # ======================================================

    IDLE = "IDLE"

    REQUEST_RECEIVED = "REQUEST_RECEIVED"

    # ======================================================
    # VALIDATION LAYER
    # ======================================================

    INPUT_VALIDATION = "INPUT_VALIDATION"

    DOMAIN_VALIDATION = "DOMAIN_VALIDATION"

    SECURITY_VALIDATION = "SECURITY_VALIDATION"

    # ======================================================
    # UNDERSTANDING LAYER
    # ======================================================

    INTENT_CLASSIFICATION = "INTENT_CLASSIFICATION"

    ENTITY_EXTRACTION = "ENTITY_EXTRACTION"

    CONTEXT_ANALYSIS = "CONTEXT_ANALYSIS"

    TASK_DECOMPOSITION = "TASK_DECOMPOSITION"

    # ======================================================
    # MEMORY LAYER
    # ======================================================

    MEMORY_RETRIEVAL = "MEMORY_RETRIEVAL"

    MEMORY_ANALYSIS = "MEMORY_ANALYSIS"

    MEMORY_UPDATE = "MEMORY_UPDATE"

    # ======================================================
    # REASONING LAYER
    # ======================================================

    GOAL_IDENTIFICATION = "GOAL_IDENTIFICATION"

    PLAN_GENERATION = "PLAN_GENERATION"

    DECISION_MAKING = "DECISION_MAKING"

    # ======================================================
    # TOOL LAYER
    # ======================================================

    TOOL_SELECTION = "TOOL_SELECTION"

    TOOL_EXECUTION = "TOOL_EXECUTION"

    TOOL_VALIDATION = "TOOL_VALIDATION"

    # ======================================================
    # RESPONSE LAYER
    # ======================================================

    PROMPT_CONSTRUCTION = "PROMPT_CONSTRUCTION"

    RESPONSE_GENERATION = "RESPONSE_GENERATION"

    RESPONSE_VALIDATION = "RESPONSE_VALIDATION"

    RESPONSE_ENHANCEMENT = "RESPONSE_ENHANCEMENT"

    # ======================================================
    # REFLECTION LAYER
    # ======================================================

    SELF_REFLECTION = "SELF_REFLECTION"

    QUALITY_EVALUATION = "QUALITY_EVALUATION"

    # ======================================================
    # COMPLETION
    # ======================================================

    COMPLETED = "COMPLETED"

    # ======================================================
    # FAILURE STATES
    # ======================================================

    VALIDATION_FAILED = "VALIDATION_FAILED"

    CLASSIFICATION_FAILED = "CLASSIFICATION_FAILED"

    MEMORY_FAILED = "MEMORY_FAILED"

    TOOL_FAILED = "TOOL_FAILED"

    LLM_FAILED = "LLM_FAILED"

    RESPONSE_FAILED = "RESPONSE_FAILED"

    FAILED = "FAILED"