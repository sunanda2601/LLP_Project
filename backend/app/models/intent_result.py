from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class IntentResult:
    intent: str
    confidence: float
    goal: str = ""
    learning_level: str = "Unknown"
    duration: str = ""
    tasks: List[str] = field(default_factory=list)
    entities: List[Dict[str, str]] = field(default_factory=list)
