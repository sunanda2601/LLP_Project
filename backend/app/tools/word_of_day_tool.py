"""
===========================================================
LANGUAGE LEARNING PAL WORD OF DAY TOOL

Purpose:
- Generate Daily Vocabulary
- Improve Vocabulary Learning
- Educational Assistance

===========================================================
"""

import random

from app.models.tool_result import ToolResult


class WordOfDayTool:

    WORDS = [

        {
            "word": "Perseverance",
            "meaning": (
                "Continued effort despite "
                "difficulty or delay."
            ),
            "example": (
                "Her perseverance helped "
                "her achieve success."
            )
        },

        {
            "word": "Resilient",
            "meaning": (
                "Able to recover quickly "
                "from difficulties."
            ),
            "example": (
                "She remained resilient "
                "during tough times."
            )
        },

        {
            "word": "Eloquent",
            "meaning": (
                "Fluent and persuasive "
                "in speaking or writing."
            ),
            "example": (
                "He gave an eloquent speech."
            )
        },

        {
            "word": "Meticulous",
            "meaning": (
                "Showing great attention "
                "to detail."
            ),
            "example": (
                "She is meticulous in "
                "her work."
            )
        },

        {
            "word": "Ambiguous",
            "meaning": (
                "Open to more than one "
                "interpretation."
            ),
            "example": (
                "The statement was "
                "ambiguous."
            )
        }
    ]

    @classmethod
    def get_word_of_day(cls):

        try:

            word = random.choice(
                cls.WORDS
            )

            return ToolResult(

                success=True,

                tool_name="WordOfDayTool",

                data=word
            )

        except Exception as e:

            return ToolResult(

                success=False,

                tool_name="WordOfDayTool",

                data=None,

                error_message=str(e)
            )