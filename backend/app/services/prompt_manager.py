"""
===========================================================
LANGUAGE LEARNING PAL PROMPT MANAGER
Version: 2.0

Purpose:
- Centralized Prompt Construction
- Context Injection
- Memory Injection
- Tool Output Integration
- Reflection Feedback Integration
- Prompt Version Management

Architecture:

System Prompt
      +
Intent Prompt
      +
Memory Context
      +
Tool Output
      +
Reflection Notes
      +
User Message
      ↓
Final Prompt

===========================================================
"""

from datetime import datetime

from app.config.agent_config import (
    AGENT_NAME,
    AGENT_VERSION,
    AGENT_DOMAIN
)


class PromptManager:

    PROMPT_VERSION = "2.0"

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    @classmethod
    def build_system_prompt(cls):

        return f"""
You are {AGENT_NAME} v{AGENT_VERSION}.

Domain:
{AGENT_DOMAIN}

Identity:
You are an intelligent AI Language Learning Agent.

Core Responsibilities:

1. Grammar Correction
2. Vocabulary Building
3. Translation
4. Pronunciation Guidance
5. Conversation Practice
6. Personalized Learning Plans
7. Synonyms and Antonyms
8. Daily Language Coaching

Response Rules:

- Be educational.
- Be accurate.
- Explain reasoning.
- Provide examples.
- Give actionable guidance.
- Encourage learning.
- Stay within domain boundaries.
- Never hallucinate information.
- Never provide misleading guidance.
- If memory context has a specified Goal and Weak Areas, customize your greeting/response to mention: "I remember your goal is [Goal] and your weak area is [Weak Areas]. Today's recommendation: [Recommendation based on their weak area/goal]."
"""

    # =====================================================
    # INTENT PROMPTS
    # =====================================================

    INTENT_PROMPTS = {

        "GRAMMAR": """
Focus on grammar correction.

Requirements:
- Correct mistakes
- Explain corrections
- Show improved version
- Give examples
""",

        "VOCABULARY": """
Focus on vocabulary development.

You MUST format your response using EXACTLY the following structure (no markdown headers like ##, just plain text with capitalized labels and capitalized list items):

Word: Perseverance

Meaning:
Continued effort to do or achieve something despite difficulties.

Part of Speech:
Noun

Example:
Her perseverance helped her achieve success.

Synonyms:
Persistence
Determination
Endurance

For other words, use the identical structure:
Word: <Capitalized Word>

Meaning:
<Definition from the tool output>

Part of Speech:
<Capitalized Part of Speech from the tool output>

Example:
<Example sentence from the tool output>

Synonyms:
<Capitalized Synonym 1>
<Capitalized Synonym 2>
<Capitalized Synonym 3>
""",

        "TRANSLATION": """
Focus on translation.

Requirements:
- Preserve meaning
- Explain nuances
- Provide natural translation
""",

        "PRONUNCIATION": """
Focus on pronunciation guidance.

Requirements:
- Explain pronunciation
- Provide phonetics
- Give speaking tips
""",

        "CONVERSATION": """
Focus on conversation practice.

Requirements:
- Maintain dialogue
- Encourage participation
- Correct mistakes politely
""",

        "LEARNING_PLAN": """
Create a structured learning roadmap.

If the tool output contains a full 'weeks' structure, you should provide a concise "Welcome Back" summary focusing on TODAY'S tasks, rather than listing all 30 days.

Include precisely these sections:
1. **Welcome Back / I remember**: Briefly state their Goal, Level, and Weak Areas. Mention progress if available.
2. **Today's Learning Plan**:
   - A breakdown of tasks for today (e.g. Grammar, Vocabulary, Pronunciation, Speaking).
   - Use the specific tasks and exercises from the tool output for 'Day 1' (or the current day if specified).
   - For Grammar: Provide 3 sentences to correct.
   - For Vocabulary: List 5 relevant words to learn with meanings.
   - For Pronunciation: List 5 words to practice.
   - For Speaking: Provide 1 specific task.
3. **Daily Goal**: 3 clear bullet points of what to achieve today.
4. **Expected Outcome**: What the user will have learned by the end of today.

Keep the tone encouraging, warm, educational, and highly structured like a supportive personal English tutor.
"""
    }

    # =====================================================
    # MEMORY CONTEXT
    # =====================================================

    @staticmethod
    def build_memory_context(memory):

        if not memory:
            return ""

        profile = memory.get(
            "profile",
            {}
        )

        progress = memory.get(
            "progress",
            {}
        )

        return f"""
================ MEMORY CONTEXT ================

Goal:
{profile.get('goal', 'Not Specified')}

Learning Level:
{profile.get('learning_level', 'Unknown')}

Weak Areas:
{profile.get('weak_areas', [])}

Strong Areas:
{profile.get('strong_areas', [])}

Progress:
{progress.get('overall_progress', 0)}%

================================================
"""

    # =====================================================
    # TOOL OUTPUT CONTEXT
    # =====================================================

    @staticmethod
    def build_tool_context(tool_output):

        if not tool_output:
            return ""

        if hasattr(tool_output, "to_dict"):
            tool_output = tool_output.to_dict()

        return f"""
================ TOOL OUTPUT ==================

{tool_output}

================================================
"""

    # =====================================================
    # REFLECTION CONTEXT
    # =====================================================

    @staticmethod
    def build_reflection_context(reflection):

        if not reflection:
            return ""

        return f"""
============= REFLECTION FEEDBACK =============

Quality Score:
{reflection.get('quality_score', 0)}

Suggestions:
{reflection.get('feedback', '')}

================================================
"""

    # =====================================================
    # INTENT CONTEXT
    # =====================================================

    @classmethod
    def build_intent_context(
        cls,
        intent
    ):

        return cls.INTENT_PROMPTS.get(
            intent,
            ""
        )

    # =====================================================
    # USER CONTEXT
    # =====================================================

    @staticmethod
    def build_user_context(
        message
    ):

        return f"""
================ USER REQUEST =================

{message}

================================================
"""

    # =====================================================
    # METADATA CONTEXT
    # =====================================================

    @classmethod
    def build_metadata_context(cls):

        return f"""
Prompt Version:
{cls.PROMPT_VERSION}

Generated At:
{datetime.utcnow().isoformat()}
"""

    # =====================================================
    # FINAL PROMPT ASSEMBLY
    # =====================================================

    @classmethod
    def build_prompt(
        cls,
        message,
        intent,
        memory=None,
        tool_output=None,
        reflection=None
    ):

        sections = [

            cls.build_system_prompt(),

            cls.build_metadata_context(),

            cls.build_intent_context(
                intent
            ),

            cls.build_memory_context(
                memory
            ),

            cls.build_tool_context(
                tool_output
            ),

            cls.build_reflection_context(
                reflection
            ),

            cls.build_user_context(
                message
            )
        ]

        return "\n\n".join(

            section.strip()

            for section in sections

            if section
        )

    # =====================================================
    # DEBUG PROMPT
    # =====================================================

    @classmethod
    def preview_prompt(
        cls,
        message,
        intent,
        memory=None
    ):

        prompt = cls.build_prompt(

            message=message,

            intent=intent,

            memory=memory
        )

        return {

            "prompt_version":
                cls.PROMPT_VERSION,

            "intent":
                intent,

            "prompt":
                prompt
        }