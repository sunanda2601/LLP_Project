from fastapi import APIRouter

from app.services.intent_engine import IntentEngine
from app.services.memory_manager import MemoryManager

router = APIRouter(
    prefix="/debug",
    tags=["Debug"]
)


@router.get("/analyze")
def analyze_message(
    user_id: str,
    message: str
):

    intent_result = IntentEngine.analyze(
        message
    )

    memory = MemoryManager.get_user_memory(
        user_id
    )

    return {

        "message": message,

        "intent":
            intent_result.intent,

        "confidence":
            intent_result.confidence,

        "memory":
            memory
    }


@router.post("/evaluate")
def evaluate(
    message: str
):

    intent = (
        IntentEngine
        .analyze(message)
    )

    return {

        "message":
            message,

        "intent":
            intent.intent,

        "confidence":
            intent.confidence
    }
