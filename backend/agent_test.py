import sys
import io
import json

# Set stdout/stderr to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, '.')

from app.services.agent_controller import AgentController
from app.services.memory_manager import MemoryManager

def test_message(user_id, message):
    print(f"\n==================================================")
    print(f"SENDING MESSAGE: '{message}'")
    print(f"==================================================")
    
    agent_response = AgentController.process(user_id=user_id, message=message)
    print(f"Success: {agent_response.success}")
    print(f"Intent: {agent_response.intent}")
    print(f"State: {agent_response.state}")
    
    # Parse the debug json response
    try:
        data = json.loads(agent_response.response)
        response_text = data.get("response", "")
        print("Response Text:")
        print(response_text)
    except Exception as e:
        print("Raw Response:", agent_response.response)
        
    print(f"Metadata: {agent_response.metadata}")

# Clear any previous memory for test user
user_id = "test_user_bench"
MemoryManager.clear_state(user_id)
MemoryManager.update_profile(user_id, "goal", "")
MemoryManager.update_profile(user_id, "learning_level", "")
MemoryManager.update_profile(user_id, "weak_areas", [])

# Run tests
test_message(user_id, "Meaning of perseverance")
test_message(user_id, "Translate hello to Telugu")
test_message(user_id, "Translate good morning to Hindi")
test_message(user_id, "Synonyms of happy")
test_message(user_id, "Antonyms of happy")
