import sys
import io
import json

# Set stdout/stderr to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, '.')

from app.services.agent_controller import AgentController
from app.services.memory_manager import MemoryManager

user_id = "benchmark_user"

# Reset user profile and memory
MemoryManager.clear_state(user_id)
MemoryManager.update_profile(user_id, "goal", "")
MemoryManager.update_profile(user_id, "learning_level", "")
MemoryManager.update_profile(user_id, "weak_areas", [])
MemoryManager.update_progress(user_id, "overall_progress", 0)

# Message sequence
messages = [
    "My goal is placements",
    "My weak areas are grammar and pronunciation",
    "I am a beginner",
    "Create a complete 30-day roadmap and tell me what I should study today."
]

for msg in messages:
    print(f"\n>>> USER: {msg}")
    res = AgentController.process(user_id, msg)
    data = json.loads(res.response)
    print(f"<<< AGENT: {data.get('response')}\n")

# Get final profile and progress status to verify memory and progress tracking
profile = MemoryManager.get_profile(user_id)
memory = MemoryManager.get_user_memory(user_id)
progress = memory.get("progress", {})

print("--- Final Verified Profile in Memory ---")
print(f"Goal: {profile.get('goal')}")
print(f"Level: {profile.get('learning_level')}")
print(f"Weak Areas: {profile.get('weak_areas')}")
print(f"Overall Progress: {progress.get('overall_progress')}%")
