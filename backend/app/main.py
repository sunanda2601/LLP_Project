from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.llm_service import generate_response
from app.services.classifier import classify_message
from app.services.prompt_builder import build_prompt
from app.services.chatbot import process_message

from app.services.agent_controller import AgentController
from app.tools.progress_tracker_tool import ProgressTrackerTool
from app.routes.chat import router as chat_router
from app.routes.admin import router as admin_router
from app.routes.debug import router as debug_router
from app.routes.auth import router as auth_router

app = FastAPI(title="Language Learning Pal API", description="AI language partner backend service", version="1.0.0")

# Setup CORS policy rules for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include sub-routers
app.include_router(chat_router)
app.include_router(admin_router)
app.include_router(debug_router)
app.include_router(auth_router)

@app.get("/")
def home():
    """
    Health check home endpoint.
    """
    return {
        "message": "Language Learning Pal API Running",
        "status": "healthy"
    }

@app.get("/chat")
def chat(message: str):
    """
    Main communication endpoint that processes natural language chat messages.
    Uses the advanced AgentController orchestrator for full capability flow.
    """
    try:
        agent_response = AgentController.process(user_id="test_user", message=message)
        return {
            "success": agent_response.success,
            "feature": agent_response.intent,
            "response": agent_response.response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/analytics")
def get_analytics():
    """
    Returns learning progress metrics for the current user.
    Matches expectations of the frontend Analytics page.
    """
    result = ProgressTrackerTool.get_progress("test_user")
    data = result.data
    return {
        "goal": data.get("goal") or "Fluent English",
        "progress": f"{data.get('progress') or 0}%",
        "words_learned": len(data.get("vocabulary_learned") or [])
    }

@app.get("/dashboard-data")
def get_dashboard_data(user_id: str = "test_user"):
    """
    Returns complete dashboard details, including learner profile,
    agent status, 30-day roadmap, today's curriculum plan,
    recent tool usage, and progress dashboard metrics.
    """
    try:
        from app.services.memory_manager import MemoryManager
        from app.services.planner import Planner
        
        # Initialize user
        MemoryManager.initialize_user(user_id)
        
        # Check if profile is complete
        has_profile = MemoryManager.has_completed_profile(user_id)
        
        if not has_profile:
            return {
                "success": True,
                "has_profile": False,
                "learner_profile": {
                    "level": "No Profile Available",
                    "goal": "Start a conversation to create your learning profile",
                    "weak_areas": [],
                    "current_day": 0,
                    "progress": 0
                },
                "roadmap": None,
                "today_plan": None,
                "tool_usage": {
                    "vocabulary": None,
                    "translation": None
                },
                "learning_analytics": {
                    "progress": 0,
                    "vocabulary_learned": 0,
                    "grammar_exercises": 0,
                    "days_completed": 0,
                    "current_streak": 0
                }
            }
        
        # Load user profile and progress
        profile = MemoryManager.get_profile(user_id)
        progress = MemoryManager.get_progress(user_id)
        current_day = MemoryManager.get_current_day(user_id)
        completed_days = MemoryManager.get_completed_days(user_id)

        # Determine dynamic roadmap names based on goal
        goal_lower = (profile.get("goal") or "Placements").lower()
        if "ielts" in goal_lower:
            w1_name, w2_name, w3_name, w4_name = "Band 7+ Structures", "Academic Vocab", "Listening & Writing", "Mock Evaluations"
        elif "placement" in goal_lower or "interview" in goal_lower:
            w1_name, w2_name, w3_name, w4_name = "Grammar Foundations", "Placement Vocabulary", "Interview Communication", "Mock Placements"
        else:
            w1_name, w2_name, w3_name, w4_name = "Conversational Basics", "General Vocab", "Clarity & Intonation", "Mock Real-world"

        roadmap = {
            "week1": {"name": w1_name, "status": "completed" if current_day > 7 else ("in-progress" if current_day >= 1 else "locked")},
            "week2": {"name": w2_name, "status": "completed" if current_day > 14 else ("in-progress" if current_day >= 8 else "locked")},
            "week3": {"name": w3_name, "status": "completed" if current_day > 21 else ("in-progress" if current_day >= 15 else "locked")},
            "week4": {"name": w4_name, "status": "completed" if current_day > 30 else ("in-progress" if current_day >= 22 else "locked")}
        }

        # Generate day plan dynamically
        day_plan = Planner.generate_day_plan(user_id, current_day)
        
        # Extract latest vocabulary and translation tool usage
        latest_vocab = MemoryManager.get_latest_tool_result(user_id, "vocabulary")
        latest_trans = MemoryManager.get_latest_tool_result(user_id, "translation")

        today_plan_data = {
            "day": current_day,
            "objective": day_plan.get("objective") or "Daily Objective",
            "tasks": day_plan.get("tasks") or [],
            "assessment": day_plan.get("assessment") or "Daily review checklist",
            "expected_outcome": day_plan.get("expected_outcome") or "Fluency improvements"
        }
            
        return {
            "success": True,
            "has_profile": True,
            "learner_profile": {
                "level": profile.get("learning_level") or "Beginner",
                "goal": profile.get("goal") or "Placements",
                "weak_areas": profile.get("weak_areas") or [],
                "current_day": current_day,
                "progress": progress.get("overall_progress") or 0.0
            },
            "roadmap": roadmap,
            "today_plan": today_plan_data,
            "tool_usage": {
                "vocabulary": latest_vocab,
                "translation": latest_trans
            },
            "learning_analytics": {
                "progress": progress.get("overall_progress") or 0.0,
                "vocabulary_learned": progress.get("vocabulary_learned") or 0,
                "grammar_exercises": progress.get("grammar_exercises") or 0,
                "days_completed": len(completed_days),
                "current_streak": progress.get("current_streak") or 0
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

from pydantic import BaseModel
from typing import List

class UpdateTasksRequest(BaseModel):
    user_id: str = "test_user"
    completed_tasks: List[str]

class CompleteDayRequest(BaseModel):
    user_id: str = "test_user"

@app.post("/update-tasks")
def update_tasks(request: UpdateTasksRequest):
    """
    Saves the list of completed task names for the active day.
    """
    try:
        from app.services.memory_manager import MemoryManager
        MemoryManager.save_current_day_completed_tasks(request.user_id, request.completed_tasks)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/complete-day")
def complete_day(request: CompleteDayRequest):
    """
    Marks the current day as completed, increments the active day, and resets task lists.
    """
    try:
        from app.services.memory_manager import MemoryManager
        
        current_day = MemoryManager.get_current_day(request.user_id)
        MemoryManager.complete_day(request.user_id)
        
        # Advance the active day
        next_day = current_day + 1
        MemoryManager.update_current_day(request.user_id, next_day)
        
        # Return updated dashboard details immediately
        return get_dashboard_data(request.user_id)
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/test-classifier")
def test_classifier(message: str):
    """
    Utility debug route to test category output classification.
    """
    feature = classify_message(message)
    return {
        "feature": feature
    }

@app.get("/test-gemini")
def test_gemini():
    """
    Utility debug route to test direct Groq/Gemini response generation.
    """
    response = generate_response("Say hello to Vikranth")
    return {
        "response": response
    }

@app.get("/test-prompt")
def test_prompt(message: str):
    """
    Utility debug route to test assembled system prompts.
    """
    feature = classify_message(message)
    prompt = build_prompt(feature, message)
    return {
        "feature": feature,
        "prompt": prompt
    }
