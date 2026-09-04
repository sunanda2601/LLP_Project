"""
===========================================================
LANGUAGE LEARNING PAL AGENT CONTEXT

Central data container shared across all agent components.

Purpose:
- Maintain state across execution lifecycle
- Share information between modules
- Improve traceability
- Support memory, planning, tools, and reflection

Used By:
- Agent Controller
- Guardrails
- Intent Engine
- Planner
- Memory Manager
- Tool Router
- LLM Service
- Reflection Engine

===========================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime

from app.models.agent_state import AgentState


@dataclass
class AgentContext:

    # ======================================================
    # USER INFORMATION
    # ======================================================

    user_id: str

    session_id: str

    message: str

    # ======================================================
    # AGENT STATE
    # ======================================================

    state: AgentState = AgentState.IDLE

    # ======================================================
    # UNDERSTANDING LAYER
    # ======================================================

    intent: str = ""

    confidence: float = 0.0

    entities: List[str] = field(default_factory=list)

    # ======================================================
    # MEMORY LAYER
    # ======================================================

    memory: Dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # REASONING LAYER
    # ======================================================

    goal: str = ""

    plan: List[str] = field(default_factory=list)

    # ======================================================
    # TOOL LAYER
    # ======================================================

    selected_tool: str = ""

    tool_name: str = None

    tool_output: Dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # RESPONSE LAYER
    # ======================================================

    prompt: str = ""

    response: str = ""

    # ======================================================
    # REFLECTION LAYER
    # ======================================================

    quality_score: float = 0.0

    reflection_notes: str = ""

    # ======================================================
    # ERROR HANDLING
    # ======================================================

    error_code: str = ""

    error_message: str = ""

    # ======================================================
    # AUDIT TRAIL
    # ======================================================

    execution_path: List[str] = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.utcnow)

    def update_state(self, state):
        self.state = state
        self.execution_path.append(state.value)

    def add_reflection(self, note):
        self.reflection_notes = note