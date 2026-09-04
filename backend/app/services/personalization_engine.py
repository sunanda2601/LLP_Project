"""
===========================================================
LANGUAGE LEARNING PAL PERSONALIZATION ENGINE

Purpose:
* Personalized Learning Experience
* Goal-Based Recommendations
* Weak Area Analysis
* Vocabulary Recommendations
* Conversation Suggestions
* Learning Path Optimization

===========================================================
"""

from app.tools.progress_tracker_tool import ProgressTrackerTool


class PersonalizationEngine:

    @staticmethod
    def get_user_profile(user_id: str):
        result = ProgressTrackerTool.get_progress(user_id)
        if not result.success:
            return None
        return result.data

    @staticmethod
    def get_learning_focus(user_id: str):
        profile = PersonalizationEngine.get_user_profile(user_id)
        if not profile:
            return []

        weak_areas = profile.get("weak_areas", [])
        recommendations = []

        for area in weak_areas:
            area = area.lower()
            if area == "grammar":
                recommendations.append("Focus on grammar correction exercises.")
            elif area == "vocabulary":
                recommendations.append("Learn 10 new words daily.")
            elif area == "pronunciation":
                recommendations.append("Practice pronunciation drills.")
            elif area == "conversation":
                recommendations.append("Engage in daily conversation practice.")

        return recommendations

    @staticmethod
    def generate_personalized_plan(user_id: str):
        profile = PersonalizationEngine.get_user_profile(user_id)
        if not profile:
            return {
                "title": "General Learning Plan",
                "tasks": [
                    "Practice English daily."
                ]
            }

        goal = profile.get("goal")
        weak_areas = profile.get("weak_areas", [])

        plan = {
            "goal": goal,
            "daily_tasks": [],
            "weekly_tasks": []
        }

        if "Grammar" in weak_areas:
            plan["daily_tasks"].append("Complete 5 grammar corrections.")
        if "Vocabulary" in weak_areas:
            plan["daily_tasks"].append("Learn 10 new words.")
        if "Pronunciation" in weak_areas:
            plan["daily_tasks"].append("Practice pronunciation for 15 minutes.")
        if "Conversation" in weak_areas:
            plan["daily_tasks"].append("Have a 10-minute English conversation.")

        plan["weekly_tasks"].append("Take a progress assessment.")

        return plan

    @staticmethod
    def recommend_vocabulary(user_id: str):
        profile = PersonalizationEngine.get_user_profile(user_id)
        vocabulary_count = (
            len(profile.get("vocabulary_learned", []))
            if profile
            else 0
        )

        if vocabulary_count < 10:
            return [
                "perseverance",
                "resilient",
                "eloquent",
                "meticulous",
                "adaptable"
            ]

        if vocabulary_count < 50:
            return [
                "ubiquitous",
                "ambiguous",
                "coherent",
                "pragmatic",
                "articulate"
            ]

        return [
            "ephemeral",
            "serendipity",
            "conundrum",
            "magnanimous",
            "ubiquitous"
        ]

    @staticmethod
    def recommend_conversation_topics(user_id: str):
        profile = PersonalizationEngine.get_user_profile(user_id)
        goal = (
            profile.get("goal")
            if profile
            else ""
        )

        if not goal:
            return [
                "Daily Routine",
                "Hobbies",
                "Travel",
                "Technology"
            ]

        goal = goal.lower()
        if "job" in goal:
            return [
                "Interview Preparation",
                "Professional Communication",
                "Workplace Discussions"
            ]

        if "fluency" in goal:
            return [
                "Current Affairs",
                "Storytelling",
                "Public Speaking"
            ]

        return [
            "General Conversation",
            "Personal Introduction",
            "Opinion Sharing"
        ]

    @staticmethod
    def generate_personalized_prompt(user_id: str):
        profile = PersonalizationEngine.get_user_profile(user_id)
        if not profile:
            return ""

        return f"""
User Goal:
{profile.get("goal")}

Weak Areas:
{profile.get("weak_areas")}

Vocabulary Learned:
{len(profile.get("vocabulary_learned", []))}

Progress:
{profile.get("progress")}

Use this information to personalize the response.
"""
