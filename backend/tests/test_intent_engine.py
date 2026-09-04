"""
===========================================================
LANGUAGE LEARNING PAL INTENT ENGINE TEST SUITE
Version: 2.0

Purpose:
- Validate Intent Classification Priority
- Validate Onboarding & Real Benchmark queries
- Ensure no classification regression occurs
===========================================================
"""

import pytest
from unittest.mock import patch, MagicMock
from app.services.intent_engine import IntentEngine
from app.services.agent_controller import AgentController
from app.services.memory_manager import MemoryManager


def test_roadmap_queries():
    test_cases = [
        "create roadmap",
        "create learning plan",
        "generate roadmap",
        "generate plan",
        "study plan",
        "what should i study",
        "what should i learn today",
        "based on my goal",
        "based on my profile",
        "using my profile",
        "30 day roadmap",
        "Create a complete 30-day English roadmap for placements.",
        "Create a personalized roadmap using my profile.",
        "What should I study today?"
    ]
    for text in test_cases:
        res = IntentEngine.classify_intent(text)
        assert res.intent == "LEARNING_PLAN", f"Expected LEARNING_PLAN for query: {text}"


def test_profile_update_queries():
    # Only if learning plan patterns are not matched
    res1 = IntentEngine.classify_intent("My goal is placements")
    assert res1.intent == "PROFILE_UPDATE"

    res2 = IntentEngine.classify_intent("My weak area is pronunciation")
    assert res2.intent == "PROFILE_UPDATE"


@patch("app.services.agent_controller.generate_response")
def test_full_onboarding_and_benchmark(mock_llm, isolated_memory):
    # Set up mock response for LLM (for the real benchmark)
    mock_llm.return_value = "Here is your 30-day roadmap. Today's task: study grammar and pronunciation."

    user_id = "benchmark_user"

    # 1. Onboard user to setup profile (via "I want to improve english")
    res = AgentController.process(user_id=user_id, message="I want to improve english")
    assert res.success is True
    assert "personalized English learning plan" in res.response
    
    # 2. Complete setup
    res = AgentController.process(user_id=user_id, message="beginner, placements, grammar")
    assert res.success is True
    assert "Profile saved." in res.response

    # 3. Add pronunciation to weak areas via Profile Update
    res = AgentController.process(user_id=user_id, message="My weak area is pronunciation")
    assert res.success is True
    assert "updated your weak area to Pronunciation" in res.response

    # 4. Memory Test: "What is my current profile?"
    # Expected:
    # Goal: Placements
    # Level: Beginner
    # Weak Areas:
    # - Grammar
    # - Pronunciation
    res = AgentController.process(user_id=user_id, message="What is my current profile?")
    assert res.success is True
    assert "Goal: Placements" in res.response
    assert "Level: Beginner" in res.response
    assert "Weak Areas:" in res.response
    assert "- Grammar" in res.response
    assert "- Pronunciation" in res.response

    # 5. Real Benchmark Test:
    # "I am a beginner preparing for placements. My weak areas are grammar and pronunciation. Create a detailed 30-day roadmap and tell me exactly what I should do today."
    res = AgentController.process(
        user_id=user_id,
        message="I am a beginner preparing for placements. My weak areas are grammar and pronunciation. Create a detailed 30-day roadmap and tell me exactly what I should do today."
    )
    assert res.success is True
    assert res.intent == "LEARNING_PLAN"


def test_dictionary_tool_direct():
    from app.tools.dictionary_tool import DictionaryTool
    res = DictionaryTool.get_meaning("perseverance")
    assert res["success"] is True
    assert res["word"] == "perseverance"
    assert res["meaning"] == "Continued effort despite difficulty."
    assert "persistence" in res["synonyms"]
    assert "determination" in res["synonyms"]
    assert "endurance" in res["synonyms"]


def test_translation_tool_direct():
    from app.tools.translation_tool import TranslationTool
    res = TranslationTool.translate("Hello", target_language="te")
    assert res["success"] is True
    assert "నమస్తే" in res["translated_text"]


def test_synonyms_and_antonyms_direct():
    from app.tools.synonym_tool import SynonymTool
    from app.tools.antonym_tool import AntonymTool
    
    res_syn = SynonymTool.get_synonyms("happy")
    assert res_syn.success is True
    assert "joyful" in res_syn.data["synonyms"]

    res_ant = AntonymTool.get_antonyms("happy")
    assert res_ant.success is True
    assert "sad" in res_ant.data["antonyms"]


def test_debug_analyze_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    response = client.get("/debug/analyze?user_id=test_user&message=meaning%20of%20perseverance")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "meaning of perseverance"
    assert data["intent"] == "VOCABULARY"
    assert "memory" in data


def test_debug_evaluate_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    response = client.post("/debug/evaluate?message=Create%20a%20learning%20plan")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Create a learning plan"
    assert data["intent"] == "LEARNING_PLAN"


def test_admin_tool_health_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    response = client.get("/admin/tool-health")
    assert response.status_code == 200
    data = response.json()
    assert data["dictionary"] is True
    assert data["translation"] is True
    assert data["pronunciation"] is True
    assert data["synonyms"] is True
    assert data["antonyms"] is True


def test_memory_query_intent_classification():
    test_cases = [
        "what are my weak areas",
        "what is my goal",
        "what is my current profile",
        "what is my profile",
        "my profile",
        "show my profile",
        "what is my weak area",
        "my weak areas"
    ]
    for text in test_cases:
        res = IntentEngine.classify_intent(text)
        assert res.intent == "MEMORY_QUERY", f"Expected MEMORY_QUERY for query: {text}"


@patch("app.services.agent_controller.generate_response")
def test_smart_onboarding_flow(mock_llm, isolated_memory):
    user_id = "smart_user"
    
    # Pre-populate goal and weak areas
    MemoryManager.save_goal(user_id, "Placements")
    MemoryManager.add_weak_area(user_id, "Grammar")
    MemoryManager.add_weak_area(user_id, "Pronunciation")
    
    # 1. User requests to improve English
    response1 = AgentController.process(
        user_id=user_id,
        message="I want to improve English"
    )
    
    assert response1.success is True
    # The agent should notice the pre-populated values and only ask for level
    assert "I already know:" in response1.response
    assert "Goal: Placements" in response1.response
    assert "Weak Areas: Grammar, Pronunciation" in response1.response
    assert "I only need your current level." in response1.response
    assert MemoryManager.get_state(user_id) == "WAITING_FOR_PROFILE"
    
    # 2. User replies with level
    response2 = AgentController.process(
        user_id=user_id,
        message="intermediate"
    )
    
    assert response2.success is True
    assert "Profile saved." in response2.response
    assert "Level: Intermediate" in response2.response
    assert "Goal: Placements" in response2.response
    assert "Weak Area: Grammar, Pronunciation" in response2.response
    assert "Your 30-Day Placement English Roadmap:" in response2.response
    
    # Check memory is complete and state is cleared
    profile = MemoryManager.get_profile(user_id)
    assert profile["learning_level"] == "Intermediate"
    assert profile["goal"] == "Placements"
    assert "Grammar" in profile["weak_areas"]
    assert "Pronunciation" in profile["weak_areas"]
    assert MemoryManager.get_state(user_id) is None
    
    # 3. Memory query for weak areas
    response3 = AgentController.process(
        user_id=user_id,
        message="What are my weak areas?"
    )
    assert response3.success is True
    assert "Your weak areas are Grammar and Pronunciation." in response3.response


