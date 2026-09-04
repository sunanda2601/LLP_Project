"""
===========================================================
LANGUAGE LEARNING PAL TOOL ROUTER TEST SUITE
Version: 2.0

Purpose:
- Tool Registration Validation
- Tool Discovery Validation
- Tool Execution Validation
- Error Handling Validation
- Result Validation

===========================================================
"""

import pytest

from app.services.tool_router import ToolRouter


# =========================================================
# TOOL REGISTRY
# =========================================================

def test_available_tools_exist():

    tools = ToolRouter.get_available_tools()

    assert isinstance(
        tools,
        list
    )

    assert len(tools) > 0


def test_tool_registry_not_empty():

    tools = ToolRouter.get_available_tools()

    assert len(tools) >= 1


# =========================================================
# TOOL EXISTENCE
# =========================================================

@pytest.mark.parametrize(

    "intent",

    [

        "TRANSLATION",

        "VOCABULARY",

        "PRONUNCIATION",

        "SYNONYMS",

        "ANTONYMS",

        "WORD_OF_DAY"
    ]
)
def test_tool_exists(intent):

    assert ToolRouter.tool_exists(
        intent
    ) is True


def test_invalid_tool_not_exists():

    assert ToolRouter.tool_exists(
        "INVALID_TOOL"
    ) is False


# =========================================================
# TOOL SELECTION
# =========================================================

def test_tool_selection_translation():

    tool = ToolRouter.select_tool(
        "TRANSLATION"
    )

    assert tool is not None


def test_tool_selection_vocabulary():

    tool = ToolRouter.select_tool(
        "VOCABULARY"
    )

    assert tool is not None


def test_tool_selection_pronunciation():

    tool = ToolRouter.select_tool(
        "PRONUNCIATION"
    )

    assert tool is not None


# =========================================================
# TOOL EXECUTION
# =========================================================

@pytest.mark.parametrize(

    "intent,payload",

    [

        (
            "TRANSLATION",
            "Hello"
        ),

        (
            "VOCABULARY",
            "Perseverance"
        ),

        (
            "PRONUNCIATION",
            "Entrepreneur"
        )
    ]
)
def test_tool_execution(
    intent,
    payload
):

    result = ToolRouter.execute_tool(

        intent=intent,

        payload=payload
    )

    assert result is not None


# =========================================================
# INVALID TOOL EXECUTION
# =========================================================

def test_invalid_tool_execution():

    result = ToolRouter.execute_tool(

        intent="INVALID_TOOL",

        payload="Hello"
    )

    assert result.success is False


# =========================================================
# EMPTY PAYLOAD
# =========================================================

def test_empty_payload():

    result = ToolRouter.execute_tool(

        intent="TRANSLATION",

        payload=""
    )

    assert result is not None


# =========================================================
# TOOL RESULT STRUCTURE
# =========================================================

def test_tool_result_structure():

    result = ToolRouter.execute_tool(

        intent="TRANSLATION",

        payload="Hello"
    )

    assert hasattr(
        result,
        "success"
    )


def test_tool_result_has_data():

    result = ToolRouter.execute_tool(

        intent="TRANSLATION",

        payload="Hello"
    )

    assert hasattr(
        result,
        "data"
    )


# =========================================================
# TOOL CONSISTENCY
# =========================================================

def test_tool_consistency():

    result1 = ToolRouter.execute_tool(

        intent="TRANSLATION",

        payload="Hello"
    )

    result2 = ToolRouter.execute_tool(

        intent="TRANSLATION",

        payload="Hello"
    )

    assert (
        result1.success
        ==
        result2.success
    )


# =========================================================
# BULK EXECUTION
# =========================================================

def test_bulk_tool_execution():

    results = []

    for _ in range(25):

        result = ToolRouter.execute_tool(

            intent="TRANSLATION",

            payload="Hello"
        )

        results.append(result)

    assert len(results) == 25


# =========================================================
# TOOL LIST VALIDATION
# =========================================================

def test_tool_list_contains_translation():

    tools = ToolRouter.get_available_tools()

    assert (
        "TRANSLATION"
        in tools
    )


def test_tool_list_contains_vocabulary():

    tools = ToolRouter.get_available_tools()

    assert (
        "VOCABULARY"
        in tools
    )


# =========================================================
# EDGE CASES
# =========================================================

def test_unicode_payload():

    result = ToolRouter.execute_tool(

        intent="TRANSLATION",

        payload="నమస్తే"
    )

    assert result is not None


def test_special_character_payload():

    result = ToolRouter.execute_tool(

        intent="TRANSLATION",

        payload="@#$%^&*"
    )

    assert result is not None


def test_long_payload():

    text = (
        "Hello " * 500
    )

    result = ToolRouter.execute_tool(

        intent="TRANSLATION",

        payload=text
    )

    assert result is not None


# =========================================================
# PERFORMANCE
# =========================================================

def test_multiple_tool_types():

    intents = [

        "TRANSLATION",

        "VOCABULARY",

        "PRONUNCIATION",

        "SYNONYMS",

        "ANTONYMS"
    ]

    for intent in intents:

        result = ToolRouter.execute_tool(

            intent=intent,

            payload="test"
        )

        assert result is not None