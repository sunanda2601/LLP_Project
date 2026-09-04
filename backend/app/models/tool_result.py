"""
===========================================================
LANGUAGE LEARNING PAL TOOL RESULT MODEL
Version: 2.0

Purpose:
- Standardized response format for all tools
- Ensures consistency across tool executions
- Provides metadata for monitoring and debugging

Used By:
- Tool Router
- Dictionary Tool
- Translation Tool
- Pronunciation Tool
- Vocabulary Tool
- Future Tools

===========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass
class ToolResult:

    # =====================================================
    # EXECUTION STATUS
    # =====================================================

    success: bool

    # =====================================================
    # TOOL INFORMATION
    # =====================================================

    tool_name: str

    tool_version: str = "1.0"

    # =====================================================
    # TOOL OUTPUT
    # =====================================================

    data: Any = None

    # =====================================================
    # MESSAGES
    # =====================================================

    message: str = ""

    # =====================================================
    # ERROR INFORMATION
    # =====================================================

    error_code: str = ""

    error_message: str = ""

    # =====================================================
    # EXECUTION METADATA
    # =====================================================

    execution_time_ms: float = 0.0

    timestamp: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

    metadata: Dict = field(
        default_factory=dict
    )

    # =====================================================
    # HELPER METHODS
    # =====================================================

    def is_success(self) -> bool:
        """
        Check whether execution succeeded.
        """

        return self.success

    def is_failure(self) -> bool:
        """
        Check whether execution failed.
        """

        return not self.success

    def to_dict(self) -> Dict:
        """
        Convert ToolResult to dictionary.
        Useful for APIs and JSON serialization.
        """

        return {

            "success": self.success,

            "tool_name": self.tool_name,

            "tool_version": self.tool_version,

            "data": self.data,

            "message": self.message,

            "error_code": self.error_code,

            "error_message": self.error_message,

            "execution_time_ms":
                self.execution_time_ms,

            "timestamp":
                self.timestamp,

            "metadata":
                self.metadata
        }