from pydantic import BaseModel
from typing import Optional


class LLMResponse(BaseModel):
    success: bool
    content: str
    provider: str = "groq"
    model: Optional[str] = None
    error: Optional[str] = None
    tokens: Optional[int] = 0
    tokens_used: Optional[int] = 0
    latency: Optional[float] = 0.0
