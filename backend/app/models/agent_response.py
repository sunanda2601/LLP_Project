"""
===========================================================
LANGUAGE LEARNING PAL AGENT RESPONSE MODEL
Version: 2.0

Purpose:
- Standardized response object
- Final output of Agent Controller
- API Response Contract
- Monitoring & Analytics Support

Used By:
- Agent Controller
- FastAPI Routes
- Frontend UI
- Logging System
- Analytics Dashboard

===========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


@dataclass
class AgentResponse:

    # =====================================================
    # RESPONSE STATUS
    # =====================================================

    success: bool

    # =====================================================
    # MAIN RESPONSE
    # =====================================================

    response: str

    # =====================================================
    # AI UNDERSTANDING
    # =====================================================

    intent: str

    confidence: float

    # =====================================================
    # AGENT STATE
    # =====================================================

    state: str

    # =====================================================
    # SESSION INFORMATION
    # =====================================================

    session_id: str = ""

    user_id: str = ""

    # =====================================================
    # QUALITY METRICS
    # =====================================================

    quality_score: float = 0.0

    reflection_passed: bool = False

    # =====================================================
    # EXECUTION DETAILS
    # =====================================================

    execution_time: float = 0.0

    execution_path: List[str] = field(
        default_factory=list
    )

    # =====================================================
    # TOOL INFORMATION
    # =====================================================

    tool_used: str = ""

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    error_code: str = ""

    error_message: str = ""

    # =====================================================
    # ADDITIONAL METADATA
    # =====================================================

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # TIMESTAMP
    # =====================================================

    timestamp: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

    # =====================================================
    # HELPER METHODS
    # =====================================================

    def is_success(self) -> bool:
        """
        Check if request succeeded.
        """
        return self.success

    def is_failure(self) -> bool:
        """
        Check if request failed.
        """
        return not self.success

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert response to dictionary.
        Useful for API responses and logging.
        """

        return {

            "success": self.success,

            "response": self.response,

            "intent": self.intent,

            "confidence": self.confidence,

            "state": self.state,

            "session_id": self.session_id,

            "user_id": self.user_id,

            "quality_score": self.quality_score,

            "reflection_passed":
                self.reflection_passed,

            "execution_time":
                self.execution_time,

            "execution_path":
                self.execution_path,

            "tool_used":
                self.tool_used,

            "error_code":
                self.error_code,

            "error_message":
                self.error_message,

            "metadata":
                self.metadata,

            "timestamp":
                self.timestamp
        }