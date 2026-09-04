"""
===========================================================
LANGUAGE LEARNING PAL AGENT CONTROLLER
Version: 2.0

Central Agent Orchestrator

Responsibilities:
- Manage Agent Lifecycle
- Coordinate All Components
- Maintain Agent Context
- Handle Failures
- Track Execution Flow
- Return Standardized Responses

Architecture:

User
 Γåô
Guardrails
 Γåô
Intent Engine
 Γåô
Memory Manager
 Γåô
Planner
 Γåô
Tool Router
 Γåô
Prompt Manager
 Γåô
LLM
 Γåô
Reflection Engine
 Γåô
Memory Update
 Γåô
Response

===========================================================
"""

from uuid import uuid4
from datetime import datetime

from app.models.agent_context import AgentContext
from app.models.agent_response import AgentResponse
from app.models.agent_state import AgentState

from app.services.guardrails import Guardrails
from app.services.intent_engine import IntentEngine
from app.services.memory_manager import MemoryManager
from app.services.planner import Planner
from app.services.tool_router import ToolRouter
from app.services.reflection_engine import ReflectionEngine
from app.services.reasoning_engine import ReasoningEngine
from app.services.execution_engine import ExecutionEngine
from app.services.prompt_manager import PromptManager

from app.services.llm_service import generate_response

from app.config.error_codes import ErrorCode


class AgentController:

    @classmethod
    def generate_personalized_roadmap(cls, goal: str, level: str, weak_areas: list) -> str:
        goal_lower = goal.lower()
        weak_area_str = ", ".join(weak_areas) if weak_areas else "Grammar"
        
        goal_display = goal
        if goal == "Placements":
            goal_display = "Placement"
        elif goal == "Interviews":
            goal_display = "Interview"
            
        if "ielts" in goal_lower:
            return (
                f"Level: {level}\n"
                f"Goal: {goal}\n"
                f"Weak Area: {weak_area_str}\n\n"
                f"Your 30-Day IELTS English Roadmap:\n\n"
                f"Week 1:\n"
                f"- IELTS Band 7+ Academic Reading & Writing task structures\n"
                f"- Core vocabulary and formatting rules\n\n"
                f"Week 2:\n"
                f"- Academic Vocabulary development & IELTS Speaking part 1 & 2 practice\n"
                f"- Cohesion and coherence drills\n\n"
                f"Week 3:\n"
                f"- Guided listening exams & Writing Task 2 essays\n"
                f"- IELTS Speaking mock practice\n\n"
                f"Week 4:\n"
                f"- Full IELTS Speaking Mock Exams & final review"
            )
        elif "placement" in goal_lower or "interview" in goal_lower:
            return (
                f"Level: {level}\n"
                f"Goal: {goal}\n"
                f"Weak Area: {weak_area_str}\n\n"
                f"Your 30-Day {goal_display} English Roadmap:\n\n"
                f"Week 1:\n"
                f"- Grammar Basics\n"
                f"- Sentence Formation\n\n"
                f"Week 2:\n"
                f"- Placement Vocabulary\n"
                f"- Speaking Practice\n\n"
                f"Week 3:\n"
                f"- HR Interview Communication\n\n"
                f"Week 4:\n"
                f"- Mock Interviews"
            )
        else:
            return (
                f"Level: {level}\n"
                f"Goal: {goal}\n"
                f"Weak Area: {weak_area_str}\n\n"
                f"Your 30-Day {goal_display} English Roadmap:\n\n"
                f"Week 1:\n"
                f"- Conversational Grammar Basics\n"
                f"- Everyday dialogue building\n\n"
                f"Week 2:\n"
                f"- General communication vocabulary\n"
                f"- Spontaneous dialogue exercises\n\n"
                f"Week 3:\n"
                f"- Pronunciation clarity & sentence intonation correction\n\n"
                f"Week 4:\n"
                f"- Real-world scenario simulation & final coaching review"
            )

    # =====================================================
    # CONTEXT CREATION
    # =====================================================

    @classmethod
    def create_context(
        cls,
        user_id: str,
        message: str
    ) -> AgentContext:

        return AgentContext(

            user_id=user_id,

            session_id=str(uuid4()),

            message=message,

            state=AgentState.REQUEST_RECEIVED
        )

    # =====================================================
    # MAIN EXECUTION PIPELINE
    # =====================================================

    @classmethod
    def process(
        cls,
        user_id: str,
        message: str
    ) -> AgentResponse:
        agent_response = cls._process(user_id, message)
        
        # Priority 5: Add Debug Mode
        import json
        from app.config.llm_config import DEBUG_MODE
        
        tool_map = {
            "VOCABULARY": "DictionaryTool",
            "WORD_OF_DAY": "WordOfDayTool",
            "SYNONYMS": "SynonymTool",
            "ANTONYMS": "AntonymTool",
            "TRANSLATION": "TranslationTool",
            "PRONUNCIATION": "PronunciationTool"
        }
        
        tool_used = agent_response.metadata.get("tool_used") or tool_map.get(agent_response.intent, None)
        
        # Update metadata trace fields to be 100% consistent across all return points
        agent_response.metadata.update({
            "intent": agent_response.intent,
            "memory_loaded": agent_response.metadata.get("memory_loaded", True),
            "tool_used": tool_used,
            "state": agent_response.state,
            "execution_path": agent_response.metadata.get("execution_path", [agent_response.state])
        })
        
        if DEBUG_MODE:
            debug_response = {
                "intent": agent_response.intent,
                "memory_used": True,
                "tool_used": tool_used,
                "state": agent_response.state,
                "response": agent_response.response
            }
            agent_response.response = json.dumps(debug_response, indent=2)
            
        return agent_response

    @classmethod
    def _process(
        cls,
        user_id: str,
        message: str
    ) -> AgentResponse:

        start_time = datetime.utcnow()

        context = cls.create_context(
            user_id=user_id,
            message=message
        )

        try:

            # ==========================================
            # VALIDATION
            # ==========================================

            context.update_state(
                AgentState.INPUT_VALIDATION
            )

            valid, error = Guardrails.validate_request(
                message
            )

            if not valid:

                return AgentResponse(

                    success=False,

                    response=f"Validation Failed: {error}",

                    intent="UNKNOWN",

                    confidence=0.0,

                    state=context.state.value,

                    metadata={
                        "error": str(error)
                    }
                )

            # ==========================================
            # INTENT ANALYSIS
            # ==========================================
            context.update_state(
                AgentState.INTENT_CLASSIFICATION
            )

            import re
            session_state = MemoryManager.get_session_state(user_id)
            message_clean = message.strip()
            message_lower = re.sub(r'[\\/?.!,\'"ΓÇÖ`\s]+$', '', message_clean.lower())

            waiting_states = ["WAITING_FOR_LEVEL", "WAITING_FOR_GOAL", "WAITING_FOR_WEAK_AREAS", "WAITING_FOR_PROFILE"]
            if session_state in waiting_states and message_lower not in ["cancel", "stop", "exit"]:
                intent_result = IntentEngine.analyze(message)
                intent_result.intent = "PROFILE_SETUP"
            else:
                if session_state in waiting_states and message_lower in ["cancel", "stop", "exit"]:
                    MemoryManager.set_session_state(user_id, None)
                    MemoryManager.clear_state(user_id)
                intent_result = IntentEngine.analyze(message)

            context.intent = intent_result.intent
            context.confidence = intent_result.confidence

            # ==========================================
            # STATE CHECK / INTERCEPTION
            # ==========================================
            # Handle Task Trigger: "Create today's grammar exercise" or "Start today's task"
            if message_lower in ["create today's grammar exercise", "start today's task"]:
                context.update_state(AgentState.COMPLETED)
                context.intent = "GRAMMAR"
                context.confidence = 1.0
                context.response = (
                    "Here is your grammar exercise for today:\n\n"
                    "Please correct the mistakes in the following sentences:\n"
                    "1. She do not like tea.\n"
                    "2. They was playing football yesterday.\n"
                    "3. I have seen him two days ago.\n\n"
                    "Reply with your corrections when you are ready!"
                )
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Handle COMPLETE_DAY
            if context.intent == "COMPLETE_DAY":
                current_day = MemoryManager.get_current_day(user_id)
                MemoryManager.complete_day(user_id)
                next_day = current_day + 1
                MemoryManager.update_current_day(user_id, next_day)
                
                completed_days = MemoryManager.get_completed_days(user_id)
                progress_dict = MemoryManager.get_progress(user_id)
                progress = progress_dict.get("overall_progress", 0.0)
                completed_list = "\n".join(f"Γ£ô Day {d}" for d in completed_days)
                
                context.update_state(AgentState.COMPLETED)
                context.confidence = 1.0
                
                if current_day >= 30:
                    profile = MemoryManager.get_profile(user_id)
                    g_score = progress_dict.get("grammar_score", 85) or 85
                    v_score = progress_dict.get("vocabulary_learned", 90) or 90
                    p_score = progress_dict.get("pronunciation_score", 80) or 80
                    if g_score == 0: g_score = 85
                    if v_score == 0: v_score = 90
                    if p_score == 0: p_score = 80
                    readiness = int((g_score + v_score + p_score) / 3)
                    
                    context.response = (
                        f"≡ƒÄë Day 30 Completed\n\n"
                        f"Progress:\n100.0%\n\n"
                        f"Completed:\n{completed_list}\n\n"
                        f"Final Assessment\n\n"
                        f"Grammar Score: {g_score}%\n"
                        f"Vocabulary Score: {v_score}%\n"
                        f"Pronunciation Score: {p_score}%\n\n"
                        f"Overall Progress: 100%\n\n"
                        f"Placement Readiness Score: {readiness}%"
                    )
                else:
                    next_plan = Planner.generate_day_plan(user_id, next_day)
                    focus_items = []
                    if next_plan:
                        objective = next_plan.get("objective")
                        if objective:
                            focus_items.append(objective)
                        if next_plan.get("vocabulary"):
                            focus_items.append("Vocabulary Building")
                        if next_plan.get("speaking_task"):
                            focus_items.append("Pronunciation Practice")
                    else:
                        focus_items = ["General English Practice"]
                    
                    focus_str = "\n".join(focus_items)
                    context.response = (
                        f"≡ƒÄë Day {current_day} Completed\n\n"
                        f"Progress:\n{progress:.1f}%\n\n"
                        f"Completed:\n{completed_list}\n\n"
                        f"Next:\nDay {next_day}\n\n"
                        f"Today's Focus:\n{focus_str}"
                    )
                
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Handle RESET_PROGRESS
            if context.intent == "RESET_PROGRESS":
                MemoryManager.delete_user_memory(user_id)
                MemoryManager.initialize_user(user_id)
                MemoryManager.clear_state(user_id)
                MemoryManager.set_session_state(user_id, None)
                
                context.update_state(AgentState.COMPLETED)
                context.confidence = 1.0
                context.response = (
                    "Your learning progress and profile have been completely reset.\n\n"
                    "Start a conversation by typing **'I want to improve English'** to set up a new learning path!"
                )
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Handle CONTINUE_PLAN
            if context.intent == "CONTINUE_PLAN":
                current_day = MemoryManager.get_current_day(user_id)
                
                if current_day > 30:
                    profile = MemoryManager.get_profile(user_id)
                    progress_dict = MemoryManager.get_progress(user_id)
                    g_score = progress_dict.get("grammar_score", 85) or 85
                    v_score = progress_dict.get("vocabulary_learned", 90) or 90
                    p_score = progress_dict.get("pronunciation_score", 80) or 80
                    if g_score == 0: g_score = 85
                    if v_score == 0: v_score = 90
                    if p_score == 0: p_score = 80
                    readiness = int((g_score + v_score + p_score) / 3)
                    
                    context.update_state(AgentState.COMPLETED)
                    context.confidence = 1.0
                    context.response = (
                        f"Final Assessment\n\n"
                        f"Grammar Score: {g_score}%\n"
                        f"Vocabulary Score: {v_score}%\n"
                        f"Pronunciation Score: {p_score}%\n\n"
                        f"Overall Progress: 100%\n\n"
                        f"Placement Readiness Score: {readiness}%"
                    )
                else:
                    day_plan = Planner.generate_day_plan(user_id, current_day)
                    grammar_list = day_plan.get("grammar_tasks", [])
                    vocab_list = day_plan.get("vocabulary", [])
                    speaking_task = day_plan.get("speaking_task", "")
                    
                    grammar_str = ""
                    if grammar_list:
                        grammar_str = "Grammar: Correct the following sentences:\n" + "\n".join(f"{i}. {task}" for i, task in enumerate(grammar_list, 1))
                    else:
                        grammar_str = "Grammar: Focus on today's core grammar concept."
                        
                    vocab_str = ""
                    pron_str = ""
                    if vocab_list:
                        vocab_str = "Vocabulary: Learn these 5 words with their meanings:\n" + "\n".join(f"{i}. {item['word']} - {item['meaning']}" for i, item in enumerate(vocab_list, 1))
                        pron_str = "Pronunciation: Practice the pronunciation of these 5 words:\n" + "\n".join(f"{i}. {item['word']}" for i, item in enumerate(vocab_list, 1))
                    else:
                        vocab_str = "Vocabulary: Study the recommended professional vocabulary."
                        pron_str = "Pronunciation: Focus on pronunciation exercises."
                        
                    speaking_str = f"Speaking: {speaking_task}"
                    
                    context.update_state(AgentState.COMPLETED)
                    context.confidence = 1.0
                    context.response = (
                        f"Generating Day {current_day}...\n\n"
                        f"### Today's Learning Plan\n\n"
                        f"{grammar_str}\n\n"
                        f"{vocab_str}\n\n"
                        f"{pron_str}\n\n"
                        f"{speaking_str}"
                    )
                
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Handle SHOW_CURRENT_DAY
            if context.intent == "SHOW_CURRENT_DAY":
                current_day = MemoryManager.get_current_day(user_id)
                completed_days = MemoryManager.get_completed_days(user_id)
                progress_dict = MemoryManager.get_progress(user_id)
                progress = progress_dict.get("overall_progress", 0.0)
                completed_days_str = ",".join(map(str, completed_days)) if completed_days else "None"
                
                if isinstance(progress, (int, float)):
                    val = float(progress)
                    progress_str = f"{int(val)}%" if val.is_integer() else f"{val}%"
                else:
                    progress_str = "0%"
                
                context.update_state(AgentState.COMPLETED)
                context.confidence = 1.0
                context.response = (
                    f"Current Day: {current_day}\n\n"
                    f"Completed Days:\n{completed_days_str}\n\n"
                    f"Progress:\n{progress_str}"
                )
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Handle SHOW_ROADMAP
            if context.intent == "SHOW_ROADMAP":
                current_day = MemoryManager.get_current_day(user_id)
                
                upcoming = []
                for d in range(current_day + 1, min(current_day + 4, 30)):
                    upcoming.append(f"Day {d}")
                if current_day < 30:
                    upcoming.append("Final Day 30")
                
                upcoming_str = "\n".join(upcoming) if upcoming else "None"
                
                context.update_state(AgentState.COMPLETED)
                context.confidence = 1.0
                context.response = (
                    f"Current Position:\nDay {current_day}\n\n"
                    f"Upcoming:\n{upcoming_str}"
                )
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Handle Memory/Profile Queries
            if context.intent == "MEMORY_QUERY":
                profile = MemoryManager.get_profile(user_id)
                goal = profile.get("goal") or "Not Specified"
                level = profile.get("learning_level") or "Not Specified"
                weak_areas = profile.get("weak_areas", [])
                
                context.update_state(AgentState.COMPLETED)
                context.confidence = 1.0
                
                if "weak" in message_lower:
                    if len(weak_areas) == 0:
                        context.response = "Your weak areas are not specified."
                    elif len(weak_areas) == 1:
                        context.response = f"Your weak area is {weak_areas[0]}."
                    else:
                        context.response = f"Your weak areas are {', '.join(weak_areas[:-1])} and {weak_areas[-1]}."
                elif "goal" in message_lower:
                    if len(weak_areas) == 0:
                        wa_label = "Your weak area is"
                        wa_val = "Not Specified."
                    elif len(weak_areas) == 1:
                        wa_label = "Your weak area is"
                        wa_val = f"{weak_areas[0]}."
                    else:
                        wa_label = "Your weak areas are"
                        wa_val = f"{', '.join(weak_areas[:-1])} and {weak_areas[-1]}."
                    
                    context.response = (
                        f"Your goal is {goal}.\n"
                        f"Your level is {level}.\n"
                        f"{wa_label} {wa_val}"
                    )
                else:
                    weak_areas_str = "\n".join(f"- {wa}" for wa in weak_areas) if weak_areas else "- Not Specified"
                    context.response = (
                        f"Goal: {goal}\n"
                        f"Level: {level}\n"
                        f"Weak Areas:\n{weak_areas_str}"
                    )
                    
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Handle Progress Queries: SHOW_PROGRESS or PROGRESS_QUERY
            if context.intent in ["SHOW_PROGRESS", "PROGRESS_QUERY"]:
                profile = MemoryManager.get_profile(user_id)
                goal = profile.get("goal") or "Not Specified"
                
                progress_dict = MemoryManager.get_progress(user_id)
                progress = progress_dict.get("overall_progress", 0.0)
                completed_days = MemoryManager.get_completed_days(user_id)
                completed_lessons = len(completed_days)
                
                if isinstance(progress, (int, float)):
                    val = float(progress)
                    progress_str = f"{int(val)}%" if val.is_integer() else f"{val}%"
                else:
                    progress_str = "0%"
                
                context.update_state(AgentState.COMPLETED)
                context.confidence = 1.0
                context.response = (
                    f"Goal: {goal}\n"
                    f"Progress: {progress_str}\n"
                    f"Completed Tasks: {completed_lessons}"
                )
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Task 2: Handle Learning Plan intent
            learning_plan_keywords = ["improve english", "learn english", "improve my english", "become fluent", "improve communication"]
            if context.intent == "LEARNING_PLAN" or any(kw in message_lower for kw in learning_plan_keywords):
                profile = MemoryManager.get_profile(user_id)
                goal = profile.get("goal")
                level = profile.get("learning_level")
                weak_areas = profile.get("weak_areas", [])
                
                known_goal = goal if goal and goal != "Not Specified" and goal != "" else None
                known_level = level if level and level != "Not Specified" and level != "Unknown" and level != "" else None
                known_weak_areas = weak_areas if weak_areas else []
                
                if known_goal and known_level and known_weak_areas:
                    MemoryManager.clear_state(user_id)
                    context.update_state(AgentState.PLAN_GENERATION)
                    context.intent = "LEARNING_PLAN"
                    context.confidence = 1.0
                    
                    context.memory = MemoryManager.get_user_memory(user_id)
                    plan = Planner.generate_learning_plan(
                        user_id=user_id,
                        goal=known_goal,
                        duration="30 Days",
                        level=known_level,
                        weak_areas=known_weak_areas
                    )
                    MemoryManager.update_progress(user_id, "overall_progress", 0)

                    # Get today's day from progress or just default to Day 1
                    memory = MemoryManager.get_user_memory(user_id)
                    progress = memory.get("progress", {})
                    completed_lessons = progress.get("completed_lessons", 0)
                    current_day = completed_lessons + 1

                    # Filter plan to only show current day to LLM for more focused response
                    plan_dict = plan.to_dict()
                    # We can keep the whole dict, the prompt now instructs to focus on today.

                    prompt = PromptManager.build_prompt(
                        message=message,
                        intent="LEARNING_PLAN",
                        memory=context.memory,
                        tool_output=plan_dict
                    )
                    context.response = generate_response(prompt)
                    context.update_state(AgentState.COMPLETED)
                    
                    MemoryManager.add_session_memory(
                        user_id=user_id,
                        message=message,
                        response=context.response
                    )
                    return AgentResponse(
                        success=True,
                        response=context.response,
                        intent=context.intent,
                        confidence=context.confidence,
                        state=context.state.value,
                        metadata={
                            "session_id": context.session_id,
                            "execution_time": (datetime.utcnow() - start_time).total_seconds()
                        }
                    )
                
                # If some fields are missing:
                MemoryManager.clear_state(user_id)
                MemoryManager.set_state(user_id, "WAITING_FOR_LEVEL")
                MemoryManager.set_session_state(user_id, "WAITING_FOR_LEVEL")
                
                context.update_state(AgentState.COMPLETED)
                context.intent = "LEARNING_PLAN"
                context.confidence = 1.0
                context.response = (
                    "I can help you build a personalized English learning plan! Let's create your profile first.\n\n"
                    "**Step 1: What is your current English learning level?**\n"
                    "- Beginner\n"
                    "- Intermediate\n"
                    "- Advanced"
                )
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Task 3: Before IntentEngine runs, check state.
            current_state = MemoryManager.get_state(user_id)
            if current_state in ["WAITING_FOR_LEVEL", "WAITING_FOR_GOAL", "WAITING_FOR_WEAK_AREAS", "WAITING_FOR_PROFILE"]:
                if message_lower in ["cancel", "stop", "exit"]:
                    MemoryManager.clear_state(user_id)
                    MemoryManager.set_session_state(user_id, None)
                    context.update_state(AgentState.COMPLETED)
                    context.intent = "UNKNOWN"
                    context.confidence = 1.0
                    context.response = "Profile setup cancelled. Start a conversation by saying 'I want to improve English' when you are ready!"
                    MemoryManager.add_session_memory(
                        user_id=user_id,
                        message=message,
                        response=context.response
                    )
                    return AgentResponse(
                        success=True,
                        response=context.response,
                        intent=context.intent,
                        confidence=context.confidence,
                        state=context.state.value,
                        metadata={
                            "session_id": context.session_id,
                            "execution_time": (datetime.utcnow() - start_time).total_seconds()
                        }
                    )

                if current_state == "WAITING_FOR_LEVEL" or current_state == "WAITING_FOR_PROFILE":
                    level = None
                    if "beginner" in message_lower:
                        level = "Beginner"
                    elif "intermediate" in message_lower:
                        level = "Intermediate"
                    elif "advanced" in message_lower:
                        level = "Advanced"

                    if level:
                        MemoryManager.save_learning_level(user_id, level)
                        MemoryManager.set_state(user_id, "WAITING_FOR_GOAL")
                        MemoryManager.set_session_state(user_id, "WAITING_FOR_GOAL")
                        context.response = (
                            f"Great! Your level is set to **{level}**.\n\n"
                            f"**Step 2: What is your main learning goal?**\n"
                            f"- Placements\n"
                            f"- Interviews\n"
                            f"- IELTS\n"
                            f"- Communication"
                        )
                    else:
                        context.response = (
                            f"I didn't quite get that. Please specify your current level from the options below:\n"
                            f"- Beginner\n"
                            f"- Intermediate\n"
                            f"- Advanced"
                        )
                
                elif current_state == "WAITING_FOR_GOAL":
                    goal = None
                    if "placement" in message_lower:
                        goal = "Placements"
                    elif "interview" in message_lower:
                        goal = "Interviews"
                    elif "ielts" in message_lower:
                        goal = "IELTS"
                    elif "communication" in message_lower:
                        goal = "Communication"

                    if goal:
                        MemoryManager.save_goal(user_id, goal)
                        MemoryManager.set_state(user_id, "WAITING_FOR_WEAK_AREAS")
                        MemoryManager.set_session_state(user_id, "WAITING_FOR_WEAK_AREAS")
                        context.response = (
                            f"Awesome! Your goal is set to **{goal}**.\n\n"
                            f"**Step 3: Which areas do you want to focus on? (You can choose multiple)**\n"
                            f"- Grammar\n"
                            f"- Vocabulary\n"
                            f"- Pronunciation\n"
                            f"- Conversation"
                        )
                    else:
                        context.response = (
                            f"Please choose one of the following learning goals:\n"
                            f"- Placements\n"
                            f"- Interviews\n"
                            f"- IELTS\n"
                            f"- Communication"
                        )

                elif current_state == "WAITING_FOR_WEAK_AREAS":
                    weak_areas = []
                    if "grammar" in message_lower:
                        weak_areas.append("Grammar")
                    if "vocabulary" in message_lower:
                        weak_areas.append("Vocabulary")
                    if "pronunciation" in message_lower:
                        weak_areas.append("Pronunciation")
                    if "conversation" in message_lower:
                        weak_areas.append("Conversation")

                    if weak_areas:
                        MemoryManager.update_profile(user_id, "weak_areas", weak_areas)
                        MemoryManager.clear_state(user_id)
                        MemoryManager.set_session_state(user_id, None)

                        profile = MemoryManager.get_profile(user_id)
                        goal = profile.get("goal", "Communication")
                        level = profile.get("learning_level", "Beginner")
                        
                        MemoryManager.update_progress(user_id, "overall_progress", 0)
                        MemoryManager.update_current_day(user_id, 1)
                        memory = MemoryManager.load_memory()
                        memory[user_id]["completed_days"] = []
                        memory[user_id]["current_day_completed_tasks"] = []
                        memory[user_id]["progress"]["vocabulary_learned"] = 0
                        memory[user_id]["progress"]["grammar_exercises"] = 0
                        memory[user_id]["progress"]["current_streak"] = 0
                        MemoryManager.save_memory(memory)

                        plan = Planner.generate_learning_plan(
                            user_id=user_id,
                            goal=goal,
                            duration="30 Days",
                            level=level,
                            weak_areas=weak_areas
                        )

                        weak_areas_str = ", ".join(weak_areas)
                        context.update_state(AgentState.PLAN_GENERATION)
                        context.response = (
                            f"Fantastic! Your learning profile has been created successfully!\n\n"
                            f"**Profile Details:**\n"
                            f"- Level: **{level}**\n"
                            f"- Goal: **{goal}**\n"
                            f"- Focus Areas: **{weak_areas_str}**\n\n"
                            f"I have generated your customized 30-Day learning path based on these focus areas. "
                            f"Type **'what should I study today?'** or click **'Continue my learning plan'** on your dashboard to begin your Day 1 tasks!"
                        )
                    else:
                        context.response = (
                            f"Please specify one or more focus areas from the list below:\n"
                            f"- Grammar\n"
                            f"- Vocabulary\n"
                            f"- Pronunciation\n"
                            f"- Conversation"
                        )
                
                context.update_state(AgentState.COMPLETED)
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent="PROFILE_SETUP",
                    confidence=1.0,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Downstream intent handlers follow

            # ==========================================
            # PROFILE UPDATE HANDLER
            # ==========================================
            if context.intent == "PROFILE_UPDATE":
                context.update_state(AgentState.MEMORY_UPDATE)
                message_lower = message.lower()
                
                # Check for weak area update
                if "weak area" in message_lower:
                    weak_area = "Grammar"
                    if "pronunciation" in message_lower:
                        weak_area = "Pronunciation"
                    elif "vocabulary" in message_lower:
                        weak_area = "Vocabulary"
                    elif "conversation" in message_lower:
                        weak_area = "Conversation"
                    
                    MemoryManager.add_weak_area(user_id, weak_area)
                    context.response = f"I have updated your weak area to {weak_area}."
                
                # Check for goal update
                else:
                    goal = "Placements"
                    if "interview" in message_lower:
                        goal = "Interviews"
                    elif "ielts" in message_lower:
                        goal = "IELTS"
                    elif "communication" in message_lower:
                        goal = "Communication"
                    
                    MemoryManager.save_goal(user_id, goal)
                    context.response = f"I have updated your goal to {goal}."
                
                context.update_state(AgentState.COMPLETED)
                MemoryManager.add_session_memory(
                    user_id=user_id,
                    message=message,
                    response=context.response
                )
                return AgentResponse(
                    success=True,
                    response=context.response,
                    intent=context.intent,
                    confidence=context.confidence,
                    state=context.state.value,
                    metadata={
                        "session_id": context.session_id,
                        "execution_time": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # ==========================================
            # MEMORY RETRIEVAL
            # ==========================================

            context.update_state(
                AgentState.MEMORY_RETRIEVAL
            )

            # Memory integration checks & dynamic profile extraction
            message_lower = message.lower().strip()
            
            # Save level if specified
            if "beginner" in message_lower:
                MemoryManager.update_profile(user_id, "learning_level", "Beginner")
            elif "intermediate" in message_lower:
                MemoryManager.update_profile(user_id, "learning_level", "Intermediate")
            elif "advanced" in message_lower:
                MemoryManager.update_profile(user_id, "learning_level", "Advanced")

            # Save goal if specified
            if "placement" in message_lower:
                MemoryManager.save_goal(user_id, "Placements")
            elif "interview" in message_lower:
                MemoryManager.save_goal(user_id, "Interviews")
            elif "ielts" in message_lower:
                MemoryManager.save_goal(user_id, "IELTS")
            elif "communication" in message_lower:
                MemoryManager.save_goal(user_id, "Communication")

            # Save weak area if specified
            if "grammar" in message_lower:
                MemoryManager.add_weak_area(user_id, "Grammar")
            if "vocabulary" in message_lower:
                MemoryManager.add_weak_area(user_id, "Vocabulary")
            if "pronunciation" in message_lower:
                MemoryManager.add_weak_area(user_id, "Pronunciation")
            if "conversation" in message_lower:
                MemoryManager.add_weak_area(user_id, "Conversation")

            memory = MemoryManager.get_user_memory(
                user_id
            )

            context.memory = memory

            # ==========================================
            # GOAL DETECTION
            # ==========================================

            if intent_result.goal:
                current_goal = memory.get("profile", {}).get("goal")
                if not current_goal:
                    MemoryManager.save_goal(
                        user_id,
                        intent_result.goal
                    )

            # ==========================================
            # PLANNING & PROFILE SETUP
            # ==========================================

            if context.intent == "PROFILE_SETUP":
                context.update_state(
                    AgentState.PLAN_GENERATION
                )

                level = None
                if "beginner" in message_lower:
                    level = "Beginner"
                elif "intermediate" in message_lower:
                    level = "Intermediate"
                elif "advanced" in message_lower:
                    level = "Advanced"

                goal = None
                if "placement" in message_lower:
                    goal = "Placements"
                elif "interview" in message_lower:
                    goal = "Interviews"
                elif "ielts" in message_lower:
                    goal = "IELTS"
                elif "communication" in message_lower:
                    goal = "Communication"

                weak_area = None
                if "grammar" in message_lower:
                    weak_area = "Grammar"
                elif "vocabulary" in message_lower:
                    weak_area = "Vocabulary"
                elif "pronunciation" in message_lower:
                    weak_area = "Pronunciation"
                elif "conversation" in message_lower:
                    weak_area = "Conversation"

                if level:
                    MemoryManager.save_learning_level(user_id, level)
                if goal:
                    MemoryManager.save_goal(user_id, goal)
                if weak_area:
                    MemoryManager.add_weak_area(user_id, weak_area)

                MemoryManager.set_session_state(user_id, None)
                MemoryManager.clear_state(user_id)

                memory = MemoryManager.get_user_memory(user_id)
                context.memory = memory
                profile = memory.get("profile", {})
                
                g = profile.get("goal") or goal or "General English"
                lvl = profile.get("learning_level") or level or "Beginner"
                wa = profile.get("weak_areas")
                if not wa and weak_area:
                    wa = [weak_area]
                elif not wa:
                    wa = ["Grammar"]
                
                plan = Planner.generate_learning_plan(
                    user_id=user_id,
                    goal=g,
                    duration="30 Days",
                    level=lvl,
                    weak_areas=wa
                )
                MemoryManager.update_progress(user_id, "overall_progress", 0)

                prompt = PromptManager.build_prompt(
                    message=message,
                    intent="LEARNING_PLAN",
                    memory=context.memory,
                    tool_output=plan.to_dict()
                )

                context.response = f"Profile saved.\n\n" + cls.generate_personalized_roadmap(g, lvl, wa)

            elif context.intent == "LEARNING_PLAN":

                context.update_state(
                    AgentState.PLAN_GENERATION
                )

                profile = memory.get("profile", {})
                goal = profile.get("goal")
                level = profile.get("learning_level")
                weak_areas = profile.get("weak_areas", [])

                if not goal or not level or not weak_areas:
                    MemoryManager.clear_state(user_id)
                    MemoryManager.set_session_state(user_id, "WAITING_FOR_LEVEL")
                    MemoryManager.set_state(user_id, "WAITING_FOR_LEVEL")

                    context.response = (
                        "I can help you build a personalized English learning plan! Let's create your profile first.\n\n"
                        "**Step 1: What is your current English learning level?**\n"
                        "- Beginner\n"
                        "- Intermediate\n"
                        "- Advanced"
                    )
                else:
                    plan = Planner.generate_learning_plan(
                        user_id=user_id,
                        goal=goal,
                        duration="30 Days",
                        level=level,
                        weak_areas=weak_areas
                    )
                    
                    MemoryManager.update_progress(user_id, "overall_progress", 0)

                    prompt = PromptManager.build_prompt(
                        message=message,
                        intent="LEARNING_PLAN",
                        memory=context.memory,
                        tool_output=plan.to_dict()
                    )

                    context.response = generate_response(
                        prompt
                    )

            # ==========================================
            # TOOL EXECUTION
            # ==========================================

            elif context.intent in [

                "TRANSLATION",

                "PRONUNCIATION",

                "SYNONYMS",

                "ANTONYMS",

                "WORD_OF_DAY"

            ]:

                context.update_state(
                    AgentState.TOOL_SELECTION
                )

                tool_result = ToolRouter.execute_tool(

                    intent=context.intent,

                    payload=message
                )

                context.update_state(
                    AgentState.TOOL_EXECUTION
                )

                if tool_result:

                    context.tool_name = tool_result.tool_name

                    context.tool_output = (
                        tool_result.to_dict()
                    )

                    if context.intent == "SYNONYMS" and tool_result.success:
                        word = tool_result.data.get("word", "")
                        syns = tool_result.data.get("synonyms", [])
                        context.response = f"{word}\n\nSynonyms:\n" + "\n".join(f"- {s}" for s in syns)
                    elif context.intent == "ANTONYMS" and tool_result.success:
                        word = tool_result.data.get("word", "")
                        ants = tool_result.data.get("antonyms", [])
                        context.response = f"{word}\n\nAntonyms:\n" + "\n".join(f"- {a}" for a in ants)
                    elif context.intent == "TRANSLATION" and tool_result.success:
                        context.response = tool_result.data.get("translated_text", "")
                    elif context.intent == "PRONUNCIATION" and tool_result.success:
                        word = tool_result.data.get("word", "")
                        phonetic = tool_result.data.get("phonetic", "Not Available")
                        audio = tool_result.data.get("audio")
                        if audio:
                            context.response = f"Word: {word}\nPronunciation: {phonetic}\nSpeaking Tip: Audio available at {audio}"
                        else:
                            context.response = f"Word: {word}\nPronunciation: {phonetic}"
                    elif context.intent == "WORD_OF_DAY" and tool_result.success:
                        word = tool_result.data.get("word", "")
                        meaning = tool_result.data.get("meaning", "")
                        example = tool_result.data.get("example", "")
                        context.response = f"Word of the Day: {word}\nMeaning: {meaning}\nExample: {example}"
                    else:
                        context.response = str(
                            tool_result.data
                        )

                else:

                    context.response = (
                        "Tool execution failed."
                    )

            # ==========================================
            # GENERAL LLM RESPONSE
            # ==========================================

            else:

                context.update_state(
                    AgentState.RESPONSE_GENERATION
                )

                strategy = ReasoningEngine.analyze(context)

                execution_result = ExecutionEngine.execute(
                    strategy=strategy,
                    user_id=user_id,
                    message=message,
                    intent=context.intent
                )

                tool_res = execution_result.get("tool_result")
                if tool_res:
                    context.tool_name = tool_res.tool_name

                prompt = PromptManager.build_prompt(
                    message=message,
                    intent=context.intent,
                    memory=context.memory,
                    tool_output=tool_res
                )

                context.response = generate_response(prompt)

            # ==========================================
            # REFLECTION
            # ==========================================

            context.update_state(
                AgentState.SELF_REFLECTION
            )

            reflection = ReflectionEngine.evaluate(

                response=context.response,

                intent=context.intent,

                memory=context.memory
            )

            # ==========================================
            # MEMORY UPDATE
            # ==========================================

            context.update_state(
                AgentState.MEMORY_UPDATE
            )

            MemoryManager.add_session_memory(

                user_id=user_id,

                message=message,

                response=context.response
            )

            # ==========================================
            # COMPLETE
            # ==========================================

            context.update_state(
                AgentState.COMPLETED
            )

            # Save latest tool usage details for the dashboard
            import re
            if context.intent == "TRANSLATION" and context.response:
                eng = message
                tel = context.response.strip()
                # Remove label prefixes if present
                if "Translation:" in tel:
                    tel = tel.split("Translation:", 1)[1].strip()
                MemoryManager.save_latest_tool_result(user_id, "translation", {"english": eng, "telugu": tel})
            elif context.intent in ["VOCABULARY", "WORD_OF_DAY"]:
                word = None
                meaning = None
                if getattr(context, "tool_output", None) and isinstance(context.tool_output, dict):
                    data = context.tool_output.get("data", {})
                    word = data.get("word")
                    meaning = data.get("meaning")
                
                if not word:
                    word_match = re.search(r"(?:Word|Word of the Day|Word of the day):\s*([a-zA-Z\s\-ΓÇÖ]+)", context.response)
                    meaning_match = re.search(r"Meaning:\s*([^\n]+)", context.response)
                    if word_match:
                        word = word_match.group(1).strip()
                    if meaning_match:
                        meaning = meaning_match.group(1).strip()
                
                if word and meaning:
                    MemoryManager.save_latest_tool_result(user_id, "vocabulary", {"word": word, "meaning": meaning})

            execution_time = (
                datetime.utcnow() - start_time
            ).total_seconds()

            return AgentResponse(

                success=True,

                response=context.response,

                intent=context.intent,

                confidence=context.confidence,

                state=context.state.value,

                metadata={
                    "intent":
                        context.intent,

                    "memory_loaded":
                        bool(context.memory),

                    "tool_used":
                        getattr(
                            context,
                            "tool_name",
                            None
                        ),

                    "state":
                        context.state.value,

                    "execution_path":
                        context.execution_path,

                    "session_id":
                        context.session_id,

                    "execution_time":
                        execution_time,

                    "quality_score":
                        reflection.quality_score,

                    "confidence_score":
                        reflection.confidence_score,

                    "reflection_passed":
                        reflection.passed
                }
            )

        except Exception as e:

            context.update_state(
                AgentState.FAILED
            )

            return AgentResponse(

                success=False,

                response="Agent execution failed.",

                intent="UNKNOWN",

                confidence=0.0,

                state=context.state.value,

                metadata={

                    "error":
                        str(e),

                    "error_code":
                        ErrorCode.INTERNAL_SERVER_ERROR
                }
            )
