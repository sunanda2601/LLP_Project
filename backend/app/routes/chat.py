"""
===========================================================
LANGUAGE LEARNING PAL CHAT ROUTES
Version: 2.0

Purpose:
- Main Chat Endpoint
- Agent Gateway
- Request Validation
- Error Handling
- Health Monitoring

===========================================================
"""

from uuid import uuid4
from datetime import datetime

from fastapi import (
    APIRouter,
    HTTPException,
    status
)

from pydantic import BaseModel

from app.services.agent_controller import AgentController


router = APIRouter(
    prefix="/chat",
    tags=["Language Learning Pal"]
)


# =========================================================
# REQUEST MODEL
# =========================================================

class ChatRequest(BaseModel):

    user_id: str

    message: str


# =========================================================
# RESPONSE MODEL
# =========================================================

class ChatResponse(BaseModel):

    success: bool

    response: str

    intent: str

    confidence: float

    state: str

    session_id: str

    timestamp: str

    metadata: dict = {}


# =========================================================
# CHAT ENDPOINT
# =========================================================

@router.post(
    "/",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    try:

        agent_response = AgentController.process(

            user_id=request.user_id,

            message=request.message
        )

        return ChatResponse(

            success=agent_response.success,

            response=agent_response.response,

            intent=agent_response.intent,

            confidence=agent_response.confidence,

            state=agent_response.state,

            session_id=agent_response.session_id
            or str(uuid4()),

            timestamp=datetime.utcnow()
            .isoformat(),

            metadata=agent_response.metadata
        )

    except Exception as e:

        raise HTTPException(

            status_code=
            status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail={

                "success": False,

                "error":
                    str(e),

                "message":
                    "Agent execution failed."
            }
        )


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/health")
async def health_check():

    return {

        "status": "healthy",

        "service":
            "Language Learning Pal",

        "version":
            "2.0",

        "timestamp":
            datetime.utcnow().isoformat()
    }


# =========================================================
# AGENT INFORMATION
# =========================================================

@router.get("/info")
async def agent_info():

    return {

        "agent_name":
            "Language Learning Pal",

        "version":
            "2.0",

        "domain":
            "Language Learning",

        "capabilities": [

            "Grammar Correction",

            "Vocabulary Building",

            "Translation",

            "Pronunciation",

            "Conversation Practice",

            "Learning Plans",

            "Synonyms",

            "Antonyms",

            "Word Of The Day"
        ]
    }


# =========================================================
# PING
# =========================================================

@router.get("/ping")
async def ping():

    return {

        "message":
            "pong"
    }