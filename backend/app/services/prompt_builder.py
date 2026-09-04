from app.prompts.master_prompt import MASTER_PROMPT
from app.prompts.vocabulary_prompt import VOCABULARY_PROMPT
from app.prompts.grammar_prompt import GRAMMAR_PROMPT
from app.prompts.translation_prompt import TRANSLATION_PROMPT
from app.prompts.daily_phrases_prompt import DAILY_PHRASES_PROMPT
from app.prompts.conversation_prompt import CONVERSATION_PROMPT
from app.prompts.pronunciation_prompt import PRONUNCIATION_PROMPT
from app.prompts.synonyms_prompt import SYNONYMS_PROMPT
from app.prompts.antonyms_prompt import ANTONYMS_PROMPT
from app.prompts.word_of_day_prompt import WORD_OF_DAY_PROMPT

def build_prompt(feature: str, user_message: str) -> str:
    """
    Constructs a comprehensive feature prompt by merging the Master Prompt instructions
    with domain-specific templates based on the classified category.
    """
    PROMPT_MAP = {
        "VOCABULARY": VOCABULARY_PROMPT,
        "GRAMMAR": GRAMMAR_PROMPT,
        "TRANSLATION": TRANSLATION_PROMPT,
        "DAILY_PHRASES": DAILY_PHRASES_PROMPT,
        "CONVERSATION": CONVERSATION_PROMPT,
        "PRONUNCIATION": PRONUNCIATION_PROMPT,
        "SYNONYMS": SYNONYMS_PROMPT,
        "ANTONYMS": ANTONYMS_PROMPT,
        "WORD_OF_DAY": WORD_OF_DAY_PROMPT
    }

    feature_prompt = PROMPT_MAP.get(feature, "")

    final_prompt = f"""
{MASTER_PROMPT}

{feature_prompt}

User Request:
{user_message}
"""
    return final_prompt
