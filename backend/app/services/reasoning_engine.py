"""
===========================================================
LANGUAGE LEARNING PAL REASONING ENGINE
Version: 2.0

Purpose:
- Determine strategy based on current AgentContext
- Decide whether memory retrieval, tools, or planning are needed
- Standardize execution parameters for the ExecutionEngine

===========================================================
"""

from app.models.agent_context import AgentContext


class ReasoningEngine:

    @classmethod
    def analyze(cls, context: AgentContext) -> dict:
        """
        Analyze current agent context to determine execution strategy.
        """
        intent = context.intent

        strategy = {
            "use_memory": True,
            "use_tools": False,
            "tool_required": None,
            "use_planning": False
        }

        if intent == "LEARNING_PLAN":
            strategy["use_planning"] = True
        elif intent in [
            "VOCABULARY",
            "TRANSLATION",
            "PRONUNCIATION",
            "SYNONYMS",
            "ANTONYMS",
            "WORD_OF_DAY"
        ]:
            strategy["use_tools"] = True
            strategy["tool_required"] = intent

        return strategy
