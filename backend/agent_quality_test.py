import sys
import io
import json

# Set stdout/stderr to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, '.')

from app.services.agent_controller import AgentController
from app.services.memory_manager import MemoryManager

user_id = "final_benchmark_user"

# Reset user profile and memory
MemoryManager.clear_state(user_id)
MemoryManager.update_profile(user_id, "goal", "")
MemoryManager.update_profile(user_id, "learning_level", "")
MemoryManager.update_profile(user_id, "weak_areas", [])
MemoryManager.update_progress(user_id, "overall_progress", 0)

# Message sequence
messages = [
    # 1. Setup profile details
    "My goal is Placements",
    "My weak areas are Grammar and Pronunciation",
    "I am a beginner",
    # 2. Query profile details (Must resolve to MEMORY_QUERY or PROGRESS_QUERY)
    "What is my goal?",
    "What are my weak areas?",
    "Show my progress",
    # 3. Test remaining tools
    "Meaning of perseverance",
    "Translate hello to Telugu",
    "Synonyms of happy",
    # 4. Learning plan / roadmap tasks (Must resolve to LEARNING_PLAN)
    "Create a learning plan",
    "What should I study today?"
]

for msg in messages:
    print(f"\n==================================================")
    print(f"SENDING MESSAGE: '{msg}'")
    print(f"==================================================")
    
    res = AgentController.process(user_id, msg)
    print(f"Success: {res.success}")
    print(f"Intent: {res.intent}")
    print(f"State: {res.state}")
    
    try:
        data = json.loads(res.response)
        response_text = data.get("response", "")
        print("Response Text:")
        print(response_text)
    except Exception as e:
        print("Raw Response:", res.response)
        
    print(f"Metadata: {res.metadata}")
