"""
===========================================================
LANGUAGE LEARNING PAL PROGRESS TRACKER TOOL

Purpose:
- Learning Progress Tracking
- Goal Tracking
- Weak Area Tracking
- Vocabulary Tracking

===========================================================
"""

from app.models.tool_result import ToolResult


class ProgressTrackerTool:

    _storage = {}

    @classmethod
    def initialize_user(cls, user_id: str):

        if user_id not in cls._storage:

            cls._storage[user_id] = {

                "goal": None,

                "weak_areas": [],

                "vocabulary_learned": [],

                "progress": 0
            }

    @classmethod
    def set_goal(

        cls,

        user_id: str,

        goal: str

    ) -> ToolResult:

        cls.initialize_user(user_id)

        cls._storage[user_id]["goal"] = goal

        return ToolResult(

            success=True,

            tool_name="ProgressTrackerTool",

            data=cls._storage[user_id]
        )

    @classmethod
    def add_weak_area(

        cls,

        user_id: str,

        area: str

    ) -> ToolResult:

        cls.initialize_user(user_id)

        if area not in cls._storage[user_id]["weak_areas"]:

            cls._storage[user_id]["weak_areas"].append(area)

        return ToolResult(

            success=True,

            tool_name="ProgressTrackerTool",

            data=cls._storage[user_id]
        )

    @classmethod
    def add_vocabulary(

        cls,

        user_id: str,

        word: str

    ) -> ToolResult:

        cls.initialize_user(user_id)

        if word not in cls._storage[user_id]["vocabulary_learned"]:

            cls._storage[user_id][
                "vocabulary_learned"
            ].append(word)

        cls._storage[user_id]["progress"] += 1

        return ToolResult(

            success=True,

            tool_name="ProgressTrackerTool",

            data=cls._storage[user_id]
        )

    @classmethod
    def get_progress(

        cls,

        user_id: str

    ) -> ToolResult:

        cls.initialize_user(user_id)

        return ToolResult(

            success=True,

            tool_name="ProgressTrackerTool",

            data=cls._storage[user_id]
        )

    @classmethod
    def generate_report(

        cls,

        user_id: str

    ) -> ToolResult:

        cls.initialize_user(user_id)

        user = cls._storage[user_id]

        report = {

            "goal":
                user["goal"],

            "weak_areas":
                user["weak_areas"],

            "vocabulary_count":
                len(
                    user["vocabulary_learned"]
                ),

            "progress":
                user["progress"]
        }

        return ToolResult(

            success=True,

            tool_name="ProgressTrackerTool",

            data=report
        )