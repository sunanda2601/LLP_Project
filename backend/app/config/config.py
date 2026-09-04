import os
from pathlib import Path
from dotenv import load_dotenv

# Load environmental configurations from the backend .env file
BACKEND_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=BACKEND_ROOT / ".env", override=False)

# Retrieve Groq API Token
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment configurations")
