"""
===========================================================
LANGUAGE LEARNING PAL TOOL SERVICE

Purpose:
- Central Tool Orchestration
- Tool Validation
- Tool Execution
- Tool Analytics

===========================================================
"""

from app.services.tool_router import ToolRouter
from app.models.tool_result import ToolResult


class ToolService:

    @staticmethod
    def execute(

        intent: str,

        payload: str

    ) -> ToolResult:

        if not ToolRouter.tool_exists(
            intent
        ):

            return ToolResult(

                success=False,

                tool_name="UNKNOWN",

                data=None,

                error=f"Unsupported tool: {intent}"
            )

        return ToolRouter.execute_tool(

            intent=intent,

            payload=payload
        )

    @staticmethod
    def available_tools():

        return ToolRouter.get_available_tools()