"""
===========================================================
LANGUAGE LEARNING PAL MEMORY MANAGER
Version: 2.0

Responsibilities:
- User Profile Memory
- Session Memory
- Long-Term Memory
- Goal Tracking
- Weak Area Tracking
- Progress Tracking
- Memory Search
- Memory Audit Trail

===========================================================
"""

import json
import uuid

from pathlib import Path
from datetime import datetime


class MemoryManager:

    MEMORY_FILE = Path(
        "app/storage/memory.json"
    )

    # =====================================================
    # CORE STORAGE
    # =====================================================

    @classmethod
    def load_memory(cls):

        if not cls.MEMORY_FILE.exists():

            cls.MEMORY_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            cls.MEMORY_FILE.write_text(
                "{}",
                encoding="utf-8"
            )

        try:

            with open(
                cls.MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:

            return {}

    @classmethod
    def save_memory(cls, memory):

        with open(
            cls.MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                memory,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =====================================================
    # USER INITIALIZATION
    # =====================================================

    @classmethod
    def initialize_user(cls, user_id):

        memory = cls.load_memory()

        if user_id not in memory:

            memory[user_id] = {

                "profile": {
                    "goal": "",
                    "learning_level": "",
                    "weak_areas": [],
                    "strong_areas": [],
                    "preferred_language": "English"
                },

                "progress": {
                    "completed_lessons": 0,
                    "vocabulary_learned": 0,
                    "grammar_score": 0,
                    "pronunciation_score": 0,
                    "conversation_score": 0,
                    "overall_progress": 0
                },

                "session_memory": [],

                "long_term_memory": [],

                "audit_log": [],

                "session_state_dict": {
                    "current_state": None,
                    "goal": None,
                    "learning_level": None,
                    "weak_areas": []
                },

                "current_day": 1,

                "completed_days": [],

                "current_day_completed_tasks": []
            }
            if "current_streak" not in memory[user_id]["progress"]:
                memory[user_id]["progress"]["current_streak"] = 0

            cls.save_memory(memory)
        else:
            changed = False
            if "current_day" not in memory[user_id]:
                memory[user_id]["current_day"] = 1
                changed = True
            if "completed_days" not in memory[user_id]:
                memory[user_id]["completed_days"] = []
                changed = True
            if "current_day_completed_tasks" not in memory[user_id]:
                memory[user_id]["current_day_completed_tasks"] = []
                changed = True
            if "current_streak" not in memory[user_id]["progress"]:
                memory[user_id]["progress"]["current_streak"] = len(memory[user_id].get("completed_days", []))
                changed = True
            if changed:
                cls.save_memory(memory)

    # =====================================================
    # PROFILE MEMORY
    # =====================================================

    @classmethod
    def update_profile(
        cls,
        user_id,
        key,
        value
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        memory[user_id]["profile"][key] = value

        cls.save_memory(memory)

    @classmethod
    def get_profile(
        cls,
        user_id
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        return memory[user_id]["profile"]

    @classmethod
    def has_completed_profile(cls, user_id) -> bool:
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        profile = memory[user_id].get("profile", {})
        goal = profile.get("goal")
        level = profile.get("learning_level")
        weak_areas = profile.get("weak_areas", [])
        return bool(goal and goal != "Not Specified" and goal != "" and level and level != "Not Specified" and level != "Unknown" and level != "" and weak_areas)


    # =====================================================
    # GOAL MANAGEMENT
    # =====================================================

    @classmethod
    def save_goal(
        cls,
        user_id,
        goal
    ):

        cls.update_profile(
            user_id,
            "goal",
            goal
        )

    @classmethod
    def get_goal(
        cls,
        user_id
    ):

        profile = cls.get_profile(user_id)

        return profile.get("goal")

    # =====================================================
    # WEAK AREA MANAGEMENT
    # =====================================================

    @classmethod
    def add_weak_area(
        cls,
        user_id,
        weak_area
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        areas = memory[user_id]["profile"]["weak_areas"]

        if weak_area not in areas:

            areas.append(weak_area)

        cls.save_memory(memory)

    @classmethod
    def get_weak_areas(
        cls,
        user_id
    ):

        profile = cls.get_profile(user_id)

        return profile.get(
            "weak_areas",
            []
        )

    # =====================================================
    # PROGRESS MANAGEMENT
    # =====================================================

    @classmethod
    def update_progress(
        cls,
        user_id,
        key,
        value
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        memory[user_id]["progress"][key] = value

        cls.save_memory(memory)

    @classmethod
    def get_progress(
        cls,
        user_id
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        return memory[user_id]["progress"]

    # =====================================================
    # SESSION MEMORY
    # =====================================================

    @classmethod
    def add_session_memory(
        cls,
        user_id,
        message,
        response
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        memory[user_id]["session_memory"].append({

            "id": str(uuid.uuid4()),

            "timestamp":
                datetime.utcnow().isoformat(),

            "message": message,

            "response": response
        })

        memory[user_id]["session_memory"] = \
            memory[user_id]["session_memory"][-100:]

        cls.save_memory(memory)

    # =====================================================
    # LONG TERM MEMORY
    # =====================================================

    @classmethod
    def add_long_term_memory(
        cls,
        user_id,
        category,
        value
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        memory[user_id]["long_term_memory"].append({

            "id": str(uuid.uuid4()),

            "timestamp":
                datetime.utcnow().isoformat(),

            "category": category,

            "value": value
        })

        cls.save_memory(memory)

    @classmethod
    def get_long_term_memory(
        cls,
        user_id
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        return memory[user_id][
            "long_term_memory"
        ]

    # =====================================================
    # MEMORY SEARCH
    # =====================================================

    @classmethod
    def search_memory(
        cls,
        user_id,
        keyword
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        results = []

        for item in memory[user_id][
            "long_term_memory"
        ]:

            if keyword.lower() in \
                    str(item).lower():

                results.append(item)

        return results

    # =====================================================
    # AUDIT LOGGING
    # =====================================================

    @classmethod
    def log_event(
        cls,
        user_id,
        event_type,
        details=None,
        description=None
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        event_details = details if details is not None else description

        memory[user_id]["audit_log"].append({

            "timestamp":
                datetime.utcnow().isoformat(),

            "event_type": event_type,

            "details": event_details
        })

        cls.save_memory(memory)

    # =====================================================
    # COMPLETE MEMORY RETRIEVAL
    # =====================================================

    @classmethod
    def get_user_memory(
        cls,
        user_id
    ):

        cls.initialize_user(user_id)

        memory = cls.load_memory()

        return memory[user_id]

    # =====================================================
    # DELETE MEMORY
    # =====================================================

    @classmethod
    def delete_user_memory(
        cls,
        user_id
    ):

        memory = cls.load_memory()

        if user_id in memory:

            del memory[user_id]

            cls.save_memory(memory)

    @classmethod
    def set_session_state(
        cls,
        user_id,
        state
    ):
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        memory[user_id]["session_state"] = state
        cls.save_memory(memory)

    @classmethod
    def get_session_state(
        cls,
        user_id
    ):
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        return memory[user_id].get("session_state")

    @classmethod
    def set_state(
        cls,
        user_id,
        state
    ):
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        if "session_state_dict" not in memory[user_id]:
            memory[user_id]["session_state_dict"] = {
                "current_state": None,
                "goal": None,
                "learning_level": None,
                "weak_areas": []
            }
        memory[user_id]["session_state_dict"]["current_state"] = state
        cls.save_memory(memory)

    @classmethod
    def get_state(
        cls,
        user_id
    ):
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        state_dict = memory[user_id].get("session_state_dict")
        if not state_dict:
            return None
        return state_dict.get("current_state")

    @classmethod
    def clear_state(
        cls,
        user_id
    ):
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        memory[user_id]["session_state_dict"] = {
            "current_state": None,
            "goal": None,
            "learning_level": None,
            "weak_areas": []
        }
        cls.save_memory(memory)

    @classmethod
    def save_learning_level(
        cls,
        user_id,
        level
    ):
        cls.update_profile(
            user_id,
            "learning_level",
            level
        )

    @classmethod
    def get_current_day(cls, user_id) -> int:
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        return memory[user_id].get("current_day", 1)

    @classmethod
    def update_current_day(cls, user_id, day_number) -> None:
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        memory[user_id]["current_day"] = day_number
        cls.save_memory(memory)

    @classmethod
    def complete_day(cls, user_id) -> None:
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        current_day = memory[user_id].get("current_day", 1)
        completed_days = memory[user_id].get("completed_days", [])
        if current_day not in completed_days:
            completed_days.append(current_day)
        memory[user_id]["completed_days"] = completed_days
        
        # increment streak
        current_streak = memory[user_id]["progress"].get("current_streak", 0)
        memory[user_id]["progress"]["current_streak"] = current_streak + 1
        
        # reset today's tasks
        memory[user_id]["current_day_completed_tasks"] = []
        
        # update progress percentage
        progress = round((len(completed_days) / 30.0) * 100, 1)
        memory[user_id]["progress"]["overall_progress"] = progress
        memory[user_id]["progress"]["completed_lessons"] = len(completed_days)
        
        cls.save_memory(memory)

    @classmethod
    def get_progress(cls, user_id) -> dict:
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        return memory[user_id]["progress"]

    @classmethod
    def get_completed_days(cls, user_id) -> list:
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        return memory[user_id].get("completed_days", [])

    @classmethod
    def get_current_day_completed_tasks(cls, user_id) -> list:
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        return memory[user_id].get("current_day_completed_tasks", [])

    @classmethod
    def save_current_day_completed_tasks(cls, user_id, tasks: list) -> None:
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        memory[user_id]["current_day_completed_tasks"] = tasks
        cls.save_memory(memory)

    @classmethod
    def save_latest_tool_result(cls, user_id, tool_name, data):
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        if "latest_tool_usage" not in memory[user_id]:
            memory[user_id]["latest_tool_usage"] = {}
        memory[user_id]["latest_tool_usage"][tool_name] = data
        cls.save_memory(memory)

    @classmethod
    def get_latest_tool_result(cls, user_id, tool_name):
        cls.initialize_user(user_id)
        memory = cls.load_memory()
        usage = memory[user_id].get("latest_tool_usage", {})
        return usage.get(tool_name)