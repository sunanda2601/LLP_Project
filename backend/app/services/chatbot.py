from app.services.classifier import classify_message
from app.services.prompt_builder import build_prompt
from app.services.llm_service import generate_response

def process_message(user_message: str) -> dict:
    """
    Main orchestration service for Language Learning Pal chatbot pipeline.
    1. Classifies message domain
    2. Builds custom engineering prompt
    3. Requests Groq API response
    """
    try:
        # Step 1: Detect intent/domain category
        feature = classify_message(user_message)

        # Step 2: Assemble dynamic prompt block
        prompt = build_prompt(feature, user_message)

        # Step 3: Query the Groq model
        response = generate_response(prompt)

        return {
            "success": True,
            "feature": feature,
            "response": response
        }
    except Exception:
        return {
            "success": False,
            "response": "An error occurred while processing your request."
        }
