"""
===========================================================
LANGUAGE LEARNING PAL LEARNING ANALYTICS ENGINE

Purpose:
- Analytics for student learning progress
- Statistics and aggregation of performance metrics
- Generating weak area insights and trend reports
===========================================================
"""

from typing import Dict, List, Any
from app.services.memory_manager import MemoryManager


class LearningAnalyticsEngine:

    @staticmethod
    def get_progress_summary(user_id: str) -> Dict[str, Any]:
        """
        Retrieves a comprehensive summary of user progress across grammar,
        vocabulary, and pronunciation.
        """
        progress_dict = MemoryManager.get_progress(user_id) or {}
        profile = MemoryManager.get_profile(user_id) or {}
        completed_days = MemoryManager.get_completed_days(user_id) or []
        
        grammar_score = progress_dict.get("grammar_score", 0)
        vocab_score = progress_dict.get("vocabulary_learned", 0)
        pron_score = progress_dict.get("pronunciation_score", 0)
        
        overall_progress = progress_dict.get("overall_progress", 0.0)
        
        return {
            "user_id": user_id,
            "goal": profile.get("goal") or "General English",
            "level": profile.get("learning_level") or "Unknown",
            "overall_progress_percentage": overall_progress,
            "completed_days_count": len(completed_days),
            "completed_days": completed_days,
            "skills": {
                "grammar": {
                    "score": grammar_score,
                    "status": "Needs Improvement" if grammar_score < 70 else "Proficient"
                },
                "vocabulary": {
                    "words_learned": vocab_score,
                    "status": "Beginner" if vocab_score < 10 else "Intermediate" if vocab_score < 50 else "Advanced"
                },
                "pronunciation": {
                    "score": pron_score,
                    "status": "Needs Practice" if pron_score < 75 else "Excellent"
                }
            }
        }

    @staticmethod
    def get_weak_areas(user_id: str) -> List[str]:
        """
        Identifies and returns areas of weakness based on scores and user profile.
        """
        profile = MemoryManager.get_profile(user_id) or {}
        weak_areas = profile.get("weak_areas", [])
        
        # Also compute weak areas dynamically based on progress scores
        progress_dict = MemoryManager.get_progress(user_id) or {}
        g_score = progress_dict.get("grammar_score")
        p_score = progress_dict.get("pronunciation_score")
        
        dynamic_weak_areas = list(weak_areas)
        
        if g_score is not None and g_score < 70 and "Grammar" not in dynamic_weak_areas:
            dynamic_weak_areas.append("Grammar")
        if p_score is not None and p_score < 70 and "Pronunciation" not in dynamic_weak_areas:
            dynamic_weak_areas.append("Pronunciation")
            
        return dynamic_weak_areas

    @staticmethod
    def get_performance_trends(user_id: str) -> Dict[str, Any]:
        """
        Computes trend direction based on completed days and recent activity logs.
        """
        completed_days = MemoryManager.get_completed_days(user_id) or []
        
        if not completed_days:
            return {
                "status": "No activity yet",
                "trend": "Stable"
            }
            
        recent_count = len(completed_days)
        if recent_count > 0:
            return {
                "status": f"{recent_count} days completed",
                "trend": "Upward" if recent_count > 5 else "Stable"
            }
            
        return {
            "status": "Inactive",
            "trend": "Stable"
        }
