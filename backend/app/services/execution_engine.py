"""
===========================================================
LANGUAGE LEARNING PAL EXECUTION ENGINE

Purpose:
* Execute Agent Strategies
* Coordinate Components
* Run Tools
* Run Planning
* Build Execution Context

===========================================================
"""

from app.services.tool_service import ToolService
from app.services.planner import Planner
from app.services.personalization_engine import PersonalizationEngine


class ExecutionEngine:

    @staticmethod
    def execute(
        strategy: dict,
        user_id: str,
        message: str,
        intent: str
    ):
        execution_result = {
            "tool_result": None,
            "plan": None,
            "personalization": None,
            "execution_log": []
        }

        # ==========================================
        # MEMORY
        # ==========================================
        if strategy.get("use_memory"):
            profile = PersonalizationEngine.get_user_profile(user_id)
            execution_result["personalization"] = profile
            execution_result["execution_log"].append("Memory Retrieved")

        # ==========================================
        # TOOLS
        # ==========================================
        if strategy.get("use_tools"):
            tool_name = strategy.get("tool_required")
            tool_result = ToolService.execute(
                intent=tool_name,
                payload=message
            )
            execution_result["tool_result"] = tool_result
            execution_result["execution_log"].append(f"Tool Executed: {tool_name}")

        # ==========================================
        # PLANNING
        # ==========================================
        if strategy.get("use_planning"):
            profile = execution_result.get("personalization")
            if profile:
                plan = Planner.create_learning_plan(
                    user_goal=profile.get("goal"),
                    weak_areas=profile.get("weak_areas", [])
                )
            else:
                plan = Planner.create_learning_plan(
                    user_goal="General English",
                    weak_areas=[]
                )
            execution_result["plan"] = plan
            execution_result["execution_log"].append("Learning Plan Generated")

        return execution_result

    @staticmethod
    def summarize_execution(execution_result: dict):
        summary = []
        if execution_result.get("tool_result"):
            summary.append("Tool Execution Completed")
        if execution_result.get("plan"):
            summary.append("Planning Completed")
        if execution_result.get("personalization"):
            summary.append("Memory Personalization Applied")
        return summary

    @staticmethod
    def execution_successful(execution_result: dict) -> bool:
        if execution_result.get("tool_result"):
            tool_result = execution_result["tool_result"]
            if hasattr(tool_result, "success"):
                return tool_result.success
        return True
