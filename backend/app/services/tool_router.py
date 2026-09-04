"""
===========================================================
LANGUAGE LEARNING PAL TOOL ROUTER
Version: 2.0

Responsibilities:
- Tool Discovery
- Tool Selection
- Tool Validation
- Tool Execution
- Error Handling
- Tool Monitoring
- Execution Tracking

===========================================================
"""

from datetime import datetime
from typing import Dict, Any, Optional

from app.models.tool_result import ToolResult

from app.tools.dictionary_tool import DictionaryTool
from app.tools.translation_tool import TranslationTool
from app.tools.pronunciation_tool import PronunciationTool
from app.tools.synonym_tool import SynonymTool
from app.tools.antonym_tool import AntonymTool
from app.tools.word_of_day_tool import WordOfDayTool
from app.agents.cultural_agent import CulturalAgent
from app.utils.text_parser import TextParser

from app.config.error_codes import ErrorCode


class ToolRouter:

    """
    Centralized Tool Management Layer
    """

    TOOL_REGISTRY = {
        "VOCABULARY": DictionaryTool,
        "WORD_OF_DAY": WordOfDayTool,
        "SYNONYMS": SynonymTool,
        "ANTONYMS": AntonymTool,
        "TRANSLATION": TranslationTool,
        "PRONUNCIATION": PronunciationTool,
        "CULTURAL": CulturalAgent
    }

    TOOL_METADATA = {
        "VOCABULARY": {
            "tool_name": "DictionaryTool",
            "version": "1.0"
        },
        "WORD_OF_DAY": {
            "tool_name": "WordOfDayTool",
            "version": "1.0"
        },
        "SYNONYMS": {
            "tool_name": "SynonymTool",
            "version": "1.0"
        },
        "ANTONYMS": {
            "tool_name": "AntonymTool",
            "version": "1.0"
        },
        "TRANSLATION": {
            "tool_name": "TranslationTool",
            "version": "1.0"
        },
        "PRONUNCIATION": {
            "tool_name": "PronunciationTool",
            "version": "1.0"
        },
        "CULTURAL": {
            "tool_name": "CulturalAgent",
            "version": "1.0"
        }
     }
    

    # =====================================================
    # TOOL DISCOVERY
    # =====================================================

    @classmethod
    def get_available_tools(cls):
        return list(cls.TOOL_REGISTRY.keys())

    @classmethod
    def tool_exists(cls, intent: str) -> bool:
        return intent in cls.TOOL_REGISTRY

    # =====================================================
    # TOOL SELECTION
    # =====================================================

    @classmethod
    def select_tool(cls, intent: str):
        return cls.TOOL_REGISTRY.get(intent)

    # =====================================================
    # PAYLOAD VALIDATION
    # =====================================================

    @staticmethod
    def validate_payload(payload):
        if payload is None:
            return False
        if isinstance(payload, str):
            if not payload.strip():
                return False
        return True

    # =====================================================
    # RESULT VALIDATION
    # =====================================================

    @staticmethod
    def validate_tool_result(result):
        if result is None:
            return False
        if not isinstance(result, ToolResult):
            return False
        return True

    # =====================================================
    # EXECUTION METADATA
    # =====================================================

    @staticmethod
    def create_execution_metadata(
        intent: str,
        payload: Any
    ) -> Dict:
        return {
            "intent": intent,
            "timestamp": datetime.utcnow().isoformat(),
            "payload_type": type(payload).__name__
        }

    # =====================================================
    # TOOL EXECUTION
    # =====================================================

    @classmethod
    def execute_tool(
        cls,
        intent: str,
        payload: Any
    ) -> Optional[ToolResult]:

        try:
            if not cls.validate_payload(payload):
                return ToolResult(
                    success=False,
                    tool_name="ToolRouter",
                    data=None,
                    message=ErrorCode.INVALID_INPUT_FORMAT
                )

            tool = cls.select_tool(intent)
            if not tool:
                return ToolResult(
                    success=False,
                    tool_name="ToolRouter",
                    data=None,
                    message=ErrorCode.TOOL_NOT_FOUND
                )

            # Route to the correct tool method dynamically
            if intent == "VOCABULARY":
                word = TextParser.extract_word(payload)
                if not word:
                    return ToolResult(
                        success=False,
                        tool_name="DictionaryTool",
                        data=None,
                        message="No word found in payload"
                    )
                res = tool.get_meaning(word)
                return ToolResult(
                    success=res.get("success", False),
                    tool_name="DictionaryTool",
                    data=res,
                    message=res.get("message", "")
                )

            elif intent == "WORD_OF_DAY":
                return tool.get_word_of_day()

            elif intent == "SYNONYMS":
                word = TextParser.extract_word(payload)
                if not word:
                    return ToolResult(
                        success=False,
                        tool_name="SynonymTool",
                        data=None,
                        message="No word found in payload"
                    )
                return tool.get_synonyms(word)

            elif intent == "ANTONYMS":
                word = TextParser.extract_word(payload)
                if not word:
                    return ToolResult(
                        success=False,
                        tool_name="AntonymTool",
                        data=None,
                        message="No word found in payload"
                    )
                return tool.get_antonyms(word)

            elif intent == "TRANSLATION":
                res = tool.translate(text=payload)
                return ToolResult(
                    success=res.get("success", False),
                    tool_name="TranslationTool",
                    data=res,
                    message=res.get("message", "")
                )

            elif intent == "PRONUNCIATION":
                word = TextParser.extract_word(payload)
                if not word:
                    return ToolResult(
                        success=False,
                        tool_name="PronunciationTool",
                        data=None,
                        message="No word found in payload"
                    )
                return tool.get_pronunciation(word)

            elif intent == "CULTURAL":
                cultural_response = tool.explain(
                    phrase=payload,
                    language="English"
                )
                return ToolResult(
                    success=bool(cultural_response),
                    tool_name="CulturalAgent",
                    data={
                        "response": cultural_response
                    },
                    message=""
                )

        except Exception as e:
            return ToolResult(
                success=False,
                tool_name="ToolRouter",
                data=None,
                message=str(e)
            )

    # =====================================================
    # SAFE EXECUTION
    # =====================================================

    @classmethod
    def safe_execute(
        cls,
        intent: str,
        payload: Any
    ) -> Dict:
        metadata = cls.create_execution_metadata(
            intent,
            payload
        )
        result = cls.execute_tool(
            intent,
            payload
        )
        return {
            "metadata": metadata,
            "result": result
        }

    # =====================================================
    # TOOL INFORMATION
    # =====================================================

    @classmethod
    def get_tool_info(
        cls,
        intent: str
    ):
        return cls.TOOL_METADATA.get(intent)

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    @classmethod
    def health_check(cls):
        return {
            "status": "healthy",
            "registered_tools": len(cls.TOOL_REGISTRY),
            "tools": cls.get_available_tools()
        }
