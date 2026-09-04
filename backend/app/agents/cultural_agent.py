"""
Cultural Language Learning Agent

Provides cultural context for language-learning phrases,
expressions, greetings, and communication situations.
"""

from app.services.llm_service import generate_response


class CulturalAgent:

    @classmethod
    def explain(cls, phrase: str, language: str = "English") -> str:
        prompt = f"""
You are a language-learning cultural assistant.

Phrase: {phrase}
Language: {language}

Explain the cultural context of this phrase for a language learner.

Include:
1. Meaning
2. When it is commonly used
3. Formal or informal usage
4. Cultural context
5. One appropriate example

Keep the explanation simple and useful for a language learner.
Do not invent specific cultural facts if you are uncertain.
"""

        return generate_response(prompt)