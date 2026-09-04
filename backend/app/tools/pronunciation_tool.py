"""
===========================================================
LANGUAGE LEARNING PAL PRONUNCIATION TOOL

Purpose:
- Pronunciation Guidance
- IPA Notation
- Audio Support
- Language Learning

===========================================================
"""

import requests

from app.models.tool_result import ToolResult


class PronunciationTool:

    BASE_URL = (
        "https://api.dictionaryapi.dev/api/v2/entries/en"
    )

    @classmethod
    def get_pronunciation(
        cls,
        word: str
    ) -> ToolResult:

        try:

            response = requests.get(
                f"{cls.BASE_URL}/{word}",
                timeout=10
            )

            if response.status_code != 200:

                return ToolResult(
                    success=False,
                    tool_name="PronunciationTool",
                    data=None,
                    error_message="Word not found"
                )

            data = response.json()[0]

            phonetic = data.get(
                "phonetic",
                "Not Available"
            )

            audio = None

            phonetics = data.get(
                "phonetics",
                []
            )

            for item in phonetics:

                if item.get("audio"):

                    audio = item["audio"]
                    break

            return ToolResult(

                success=True,

                tool_name="PronunciationTool",

                data={

                    "word": word,

                    "phonetic": phonetic,

                    "audio": audio
                }
            )

        except Exception as e:

            return ToolResult(

                success=False,

                tool_name="PronunciationTool",

                data=None,

                error_message=str(e)
            )