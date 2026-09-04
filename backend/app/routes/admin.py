"""
===========================================================
LANGUAGE LEARNING PAL ADMIN ROUTES
Version: 2.0

Purpose:
- System Monitoring
- Health Checks
- Analytics Dashboard
- Tool Monitoring
- LLM Monitoring
- Logger Monitoring
- Runtime Information

===========================================================
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.config.agent_config import (
    AGENT_NAME,
    AGENT_VERSION,
    AGENT_DOMAIN,
    SUPPORTED_INTENTS
)

from app.services.analytics_service import AnalyticsService
from app.services.logger import AgentLogger
from app.services.llm_service import LLMService
from app.services.tool_router import ToolRouter


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# =========================================================
# TOOL HEALTH
# =========================================================

@router.get("/tool-health")
def tool_health():

    return {

        "dictionary": True,

        "translation": True,

        "pronunciation": True,

        "synonyms": True,

        "antonyms": True
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/health")
async def health_check():

    try:

        return {

            "status": "healthy",

            "agent": AGENT_NAME,

            "version": AGENT_VERSION,

            "timestamp":
                datetime.utcnow().isoformat(),

            "services": {

                "analytics":
                    AnalyticsService.health_check(),

                "logger":
                    AgentLogger.health_check(),

                "llm":
                    LLMService.health_check()
            }
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# AGENT INFORMATION
# =========================================================

@router.get("/info")
async def agent_info():

    return {

        "agent_name":
            AGENT_NAME,

        "agent_version":
            AGENT_VERSION,

        "domain":
            AGENT_DOMAIN,

        "supported_intents":
            SUPPORTED_INTENTS,

        "total_supported_intents":
            len(SUPPORTED_INTENTS),

        "available_tools":
            ToolRouter.get_available_tools(),

        "total_tools":
            len(
                ToolRouter.get_available_tools()
            )
    }


# =========================================================
# ANALYTICS DASHBOARD
# =========================================================

@router.get("/analytics")
async def analytics_dashboard():

    try:

        return AnalyticsService.get_dashboard()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# SYSTEM STATUS
# =========================================================

@router.get("/status")
async def system_status():

    dashboard = (
        AnalyticsService.get_dashboard()
    )

    return {

        "agent":
            AGENT_NAME,

        "version":
            AGENT_VERSION,

        "status":
            "running",

        "total_requests":
            dashboard.get(
                "total_requests",
                0
            ),

        "successful_requests":
            dashboard.get(
                "successful_requests",
                0
            ),

        "failed_requests":
            dashboard.get(
                "failed_requests",
                0
            ),

        "success_rate":
            dashboard.get(
                "success_rate",
                0
            ),

        "average_response_time":
            dashboard.get(
                "average_response_time",
                0
            ),

        "average_quality_score":
            dashboard.get(
                "average_quality_score",
                0
            ),

        "timestamp":
            datetime.utcnow().isoformat()
    }


# =========================================================
# TOOLS
# =========================================================

@router.get("/tools")
async def tools():

    available_tools = (
        ToolRouter.get_available_tools()
    )

    return {

        "total_tools":
            len(available_tools),

        "tools":
            available_tools
    }


# =========================================================
# INTENTS
# =========================================================

@router.get("/intents")
async def intents():

    return {

        "count":
            len(
                SUPPORTED_INTENTS
            ),

        "supported_intents":
            SUPPORTED_INTENTS
    }


# =========================================================
# LLM STATUS
# =========================================================

@router.get("/llm")
async def llm_status():

    try:

        return LLMService.health_check()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# LOGGER STATUS
# =========================================================

@router.get("/logger")
async def logger_status():

    return AgentLogger.health_check()


# =========================================================
# ANALYTICS RESET
# =========================================================

@router.post("/analytics/reset")
async def reset_analytics():

    try:

        AnalyticsService.reset()

        AgentLogger.info(
            "Analytics reset successfully"
        )

        return {

            "success": True,

            "message":
                "Analytics reset successfully."
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# SYSTEM SUMMARY
# =========================================================

@router.get("/summary")
async def system_summary():

    dashboard = (
        AnalyticsService.get_dashboard()
    )

    return {

        "agent": {

            "name":
                AGENT_NAME,

            "version":
                AGENT_VERSION,

            "domain":
                AGENT_DOMAIN
        },

        "analytics": dashboard,

        "tools": {

            "count":
                len(
                    ToolRouter
                    .get_available_tools()
                ),

            "available":
                ToolRouter
                .get_available_tools()
        },

        "intents": {

            "count":
                len(
                    SUPPORTED_INTENTS
                ),

            "supported":
                SUPPORTED_INTENTS
        },

        "llm": (
            LLMService.health_check()
        ),

        "logger": (
            AgentLogger.health_check()
        ),

        "generated_at":
            datetime.utcnow().isoformat()
    }