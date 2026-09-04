"""
===========================================================
LANGUAGE LEARNING PAL PLANNER TEST SUITE
Version: 2.0
===========================================================
"""

import pytest
from app.services.planner import Planner
from app.services.memory_manager import MemoryManager

def test_generate_day_plan_valid(isolated_memory):
    user_id = "planner_test_user"
    MemoryManager.save_goal(user_id, "Placements")
    MemoryManager.save_learning_level(user_id, "Intermediate")
    MemoryManager.add_weak_area(user_id, "Grammar")

    # Test Day 1
    day1_plan = Planner.generate_day_plan(user_id, 1)
    assert day1_plan is not None
    assert day1_plan["day"] == 1
    assert "objective" in day1_plan
    assert isinstance(day1_plan["grammar_tasks"], list)
    assert len(day1_plan["grammar_tasks"]) > 0
    assert isinstance(day1_plan["vocabulary"], list)
    assert "speaking_task" in day1_plan

    # Test Day 8 (Week 2)
    day8_plan = Planner.generate_day_plan(user_id, 8)
    assert day8_plan["day"] == 8
    assert day8_plan["objective"] != ""
    assert len(day8_plan["grammar_tasks"]) >= 0

def test_generate_day_plan_invalid(isolated_memory):
    user_id = "planner_test_user"
    MemoryManager.save_goal(user_id, "Placements")
    
    # Test Day 0
    day0_plan = Planner.generate_day_plan(user_id, 0)
    assert day0_plan == {}

    # Test Day 31
    day31_plan = Planner.generate_day_plan(user_id, 31)
    assert day31_plan == {}
