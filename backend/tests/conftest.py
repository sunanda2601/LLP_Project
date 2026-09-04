"""
===========================================================
LANGUAGE LEARNING PAL TEST CONFIGURATION
Version: 2.0

Purpose:
- Shared Test Fixtures
- Test Isolation
- Temporary Storage
- Mock Data Generation

Used By:
- All pytest test files

===========================================================
"""

import json
import pytest

from pathlib import Path
from uuid import uuid4

from app.services.memory_manager import MemoryManager
from app.services.analytics_service import AnalyticsService


# =========================================================
# USER FIXTURES
# =========================================================

@pytest.fixture
def test_user():

    return f"test_user_{uuid4().hex[:8]}"


@pytest.fixture
def test_session():

    return f"session_{uuid4().hex[:8]}"


# =========================================================
# MESSAGE FIXTURES
# =========================================================

@pytest.fixture
def grammar_message():

    return "Correct this sentence: I goed to school."


@pytest.fixture
def translation_message():

    return "Translate hello to Telugu."


@pytest.fixture
def vocabulary_message():

    return "What is the meaning of perseverance?"


@pytest.fixture
def conversation_message():

    return "Practice English conversation with me."


# =========================================================
# MEMORY FIXTURE
# =========================================================

@pytest.fixture
def isolated_memory(tmp_path):

    memory_file = tmp_path / "memory.json"

    MemoryManager.MEMORY_FILE = memory_file

    MemoryManager.initialize_user(
        "test_user"
    )

    return memory_file


# =========================================================
# ANALYTICS FIXTURE
# =========================================================

@pytest.fixture
def isolated_analytics(tmp_path):

    analytics_file = (
        tmp_path / "analytics.json"
    )

    AnalyticsService.ANALYTICS_FILE = (
        analytics_file
    )

    AnalyticsService.initialize()

    return analytics_file


# =========================================================
# PROFILE FIXTURE
# =========================================================

@pytest.fixture
def sample_profile():

    return {

        "goal":
            "Improve Spoken English",

        "learning_level":
            "Intermediate",

        "weak_areas": [

            "Grammar",

            "Pronunciation"
        ],

        "strong_areas": [

            "Vocabulary"
        ]
    }


# =========================================================
# MEMORY DATA FIXTURE
# =========================================================

@pytest.fixture
def sample_memory():

    return {

        "profile": {

            "goal":
                "Improve Spoken English",

            "learning_level":
                "Intermediate",

            "weak_areas": [

                "Grammar",

                "Pronunciation"
            ],

            "strong_areas": [

                "Vocabulary"
            ]
        },

        "progress": {

            "completed_lessons": 5,

            "overall_progress": 25
        },

        "session_memory": [],

        "long_term_memory": []
    }


# =========================================================
# TOOL OUTPUT FIXTURE
# =========================================================

@pytest.fixture
def sample_tool_output():

    return {

        "word":
            "Perseverance",

        "meaning":
            "Continued effort despite difficulties."
    }


# =========================================================
# REFLECTION FIXTURE
# =========================================================

@pytest.fixture
def sample_reflection():

    return {

        "quality_score": 0.92,

        "confidence_score": 0.90,

        "feedback":
            "Good educational response.",

        "passed": True
    }


# =========================================================
# CHAT REQUEST FIXTURE
# =========================================================

@pytest.fixture
def sample_chat_request():

    return {

        "user_id":
            "test_user",

        "message":
            "Translate hello to Telugu"
    }


# =========================================================
# TEMP STORAGE FIXTURE
# =========================================================

@pytest.fixture
def temp_storage(tmp_path):

    storage = (
        tmp_path / "storage"
    )

    storage.mkdir()

    return storage


# =========================================================
# CLEANUP
# =========================================================

@pytest.fixture(autouse=True)
def cleanup():

    yield

    # Future cleanup logic can go here