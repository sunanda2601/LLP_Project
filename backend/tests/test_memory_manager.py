"""
===========================================================
LANGUAGE LEARNING PAL MEMORY MANAGER TEST SUITE
Version: 2.0

Purpose:
- User Initialization
- Profile Management
- Goal Management
- Weak Area Tracking
- Progress Tracking
- Session Memory
- Long-Term Memory
- Memory Search
- Audit Logging
- Memory Cleanup
- Edge Case Validation

===========================================================
"""

import pytest

from app.services.memory_manager import MemoryManager


# =========================================================
# USER INITIALIZATION
# =========================================================

def test_initialize_user(
    test_user,
    isolated_memory
):

    MemoryManager.initialize_user(
        test_user
    )

    memory = (
        MemoryManager.load_memory()
    )

    assert test_user in memory


def test_duplicate_user_initialization(
    test_user,
    isolated_memory
):

    MemoryManager.initialize_user(
        test_user
    )

    MemoryManager.initialize_user(
        test_user
    )

    memory = (
        MemoryManager.load_memory()
    )

    assert test_user in memory


# =========================================================
# PROFILE MANAGEMENT
# =========================================================

def test_update_profile_goal(
    test_user,
    isolated_memory
):

    MemoryManager.update_profile(

        test_user,

        "goal",

        "Improve Spoken English"
    )

    profile = (
        MemoryManager.get_profile(
            test_user
        )
    )

    assert (
        profile["goal"]
        ==
        "Improve Spoken English"
    )


def test_update_learning_level(
    test_user,
    isolated_memory
):

    MemoryManager.update_profile(

        test_user,

        "learning_level",

        "Intermediate"
    )

    profile = (
        MemoryManager.get_profile(
            test_user
        )
    )

    assert (
        profile["learning_level"]
        ==
        "Intermediate"
    )


def test_get_profile_returns_dict(
    test_user,
    isolated_memory
):

    profile = (
        MemoryManager.get_profile(
            test_user
        )
    )

    assert isinstance(
        profile,
        dict
    )


# =========================================================
# GOAL MANAGEMENT
# =========================================================

def test_save_goal(
    test_user,
    isolated_memory
):

    MemoryManager.save_goal(

        test_user,

        "Fluent English"
    )

    goal = (
        MemoryManager.get_goal(
            test_user
        )
    )

    assert goal == "Fluent English"


def test_update_goal(
    test_user,
    isolated_memory
):

    MemoryManager.save_goal(
        test_user,
        "Basic English"
    )

    MemoryManager.save_goal(
        test_user,
        "Advanced English"
    )

    goal = (
        MemoryManager.get_goal(
            test_user
        )
    )

    assert goal == "Advanced English"


# =========================================================
# WEAK AREAS
# =========================================================

def test_add_weak_area(
    test_user,
    isolated_memory
):

    MemoryManager.add_weak_area(

        test_user,

        "Grammar"
    )

    weak_areas = (

        MemoryManager
        .get_weak_areas(
            test_user
        )
    )

    assert "Grammar" in weak_areas


def test_no_duplicate_weak_area(
    test_user,
    isolated_memory
):

    MemoryManager.add_weak_area(
        test_user,
        "Grammar"
    )

    MemoryManager.add_weak_area(
        test_user,
        "Grammar"
    )

    weak_areas = (

        MemoryManager
        .get_weak_areas(
            test_user
        )
    )

    assert (
        weak_areas.count(
            "Grammar"
        )
        <= 1
    )


# =========================================================
# PROGRESS MANAGEMENT
# =========================================================

def test_update_progress(
    test_user,
    isolated_memory
):

    MemoryManager.update_progress(

        test_user,

        "overall_progress",

        70
    )

    progress = (
        MemoryManager.get_progress(
            test_user
        )
    )

    assert (
        progress[
            "overall_progress"
        ]
        == 70
    )


def test_progress_returns_dict(
    test_user,
    isolated_memory
):

    progress = (
        MemoryManager.get_progress(
            test_user
        )
    )

    assert isinstance(
        progress,
        dict
    )


# =========================================================
# SESSION MEMORY
# =========================================================

def test_add_session_memory(
    test_user,
    isolated_memory
):

    MemoryManager.add_session_memory(

        user_id=test_user,

        message="Hello",

        response="Hi"
    )

    memory = (
        MemoryManager
        .get_user_memory(
            test_user
        )
    )

    assert (
        len(
            memory[
                "session_memory"
            ]
        )
        > 0
    )


def test_multiple_session_memories(
    test_user,
    isolated_memory
):

    MemoryManager.add_session_memory(
        test_user,
        "Hi",
        "Hello"
    )

    MemoryManager.add_session_memory(
        test_user,
        "Translate",
        "Translation"
    )

    memory = (
        MemoryManager
        .get_user_memory(
            test_user
        )
    )

    assert (
        len(
            memory[
                "session_memory"
            ]
        )
        >= 2
    )


# =========================================================
# LONG TERM MEMORY
# =========================================================

def test_add_long_term_memory(
    test_user,
    isolated_memory
):

    MemoryManager.add_long_term_memory(

        user_id=test_user,

        category="VOCABULARY",

        value="Perseverance"
    )

    memories = (

        MemoryManager
        .get_long_term_memory(
            test_user
        )
    )

    assert len(memories) > 0


def test_search_memory(
    test_user,
    isolated_memory
):

    MemoryManager.add_long_term_memory(

        test_user,

        "VOCABULARY",

        "Perseverance"
    )

    results = (
        MemoryManager.search_memory(

            test_user,

            "Perseverance"
        )
    )

    assert len(results) > 0


# =========================================================
# AUDIT LOGGING
# =========================================================

def test_log_event(
    test_user,
    isolated_memory
):

    MemoryManager.log_event(

        user_id=test_user,

        event_type="LOGIN",

        description="User login"
    )

    memory = (
        MemoryManager
        .get_user_memory(
            test_user
        )
    )

    assert (
        len(
            memory[
                "audit_log"
            ]
        )
        > 0
    )


# =========================================================
# USER MEMORY
# =========================================================

def test_get_user_memory(
    test_user,
    isolated_memory
):

    memory = (
        MemoryManager.get_user_memory(
            test_user
        )
    )

    assert isinstance(
        memory,
        dict
    )


# =========================================================
# DELETE MEMORY
# =========================================================

def test_delete_user_memory(
    test_user,
    isolated_memory
):

    MemoryManager.initialize_user(
        test_user
    )

    MemoryManager.delete_user_memory(
        test_user
    )

    memory = (
        MemoryManager.load_memory()
    )

    assert test_user not in memory


# =========================================================
# EDGE CASES
# =========================================================

def test_unknown_user_profile():

    profile = (
        MemoryManager.get_profile(
            "unknown_user"
        )
    )

    assert profile is not None


def test_empty_goal(
    test_user,
    isolated_memory
):

    MemoryManager.save_goal(
        test_user,
        ""
    )

    goal = (
        MemoryManager.get_goal(
            test_user
        )
    )

    assert goal == ""


def test_special_characters_goal(
    test_user,
    isolated_memory
):

    goal_text = (
        "@#$%^ Improve English!"
    )

    MemoryManager.save_goal(
        test_user,
        goal_text
    )

    goal = (
        MemoryManager.get_goal(
            test_user
        )
    )

    assert goal == goal_text


def test_memory_file_exists(
    isolated_memory
):

    assert (
        MemoryManager
        .MEMORY_FILE
        .exists()
    )


# =========================================================
# STRESS TEST
# =========================================================

def test_large_memory_insert(
    test_user,
    isolated_memory
):

    for i in range(100):

        MemoryManager.add_session_memory(

            test_user,

            f"message_{i}",

            f"response_{i}"
        )

    memory = (
        MemoryManager
        .get_user_memory(
            test_user
        )
    )

    assert (
        len(
            memory[
                "session_memory"
            ]
        )
        >= 100
    )


# =========================================================
# STATE MANAGEMENT
# =========================================================

def test_state_management(
    test_user,
    isolated_memory
):
    # Initial state should be None
    assert MemoryManager.get_state(test_user) is None

    # Set state
    MemoryManager.set_state(test_user, "WAITING_FOR_PROFILE")
    assert MemoryManager.get_state(test_user) == "WAITING_FOR_PROFILE"

    # Clear state
    MemoryManager.clear_state(test_user)
    assert MemoryManager.get_state(test_user) is None


# =========================================================
# DAY & PROGRESS TRACKING
# =========================================================

def test_day_and_progress_tracking(test_user, isolated_memory):
    # Check default day is 1
    assert MemoryManager.get_current_day(test_user) == 1
    assert MemoryManager.get_completed_days(test_user) == []
    assert MemoryManager.get_progress(test_user)["overall_progress"] == 0.0

    # Update day
    MemoryManager.update_current_day(test_user, 2)
    assert MemoryManager.get_current_day(test_user) == 2

    # Complete day 2
    MemoryManager.complete_day(test_user)
    assert MemoryManager.get_completed_days(test_user) == [2]
    # 1 day completed / 30 = 3.3%
    assert MemoryManager.get_progress(test_user)["overall_progress"] == 3.3
    
    # Progress check on profile object directly (backward compatibility)
    progress_dict = MemoryManager.get_progress(test_user)
    assert isinstance(progress_dict, dict)
    assert progress_dict["overall_progress"] == 3.3
