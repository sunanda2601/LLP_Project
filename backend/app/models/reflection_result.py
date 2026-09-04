"""
===========================================================
LANGUAGE LEARNING PAL REFLECTION RESULT MODEL
Version: 2.0

Purpose:
- Standardized output of Reflection Engine
- Response Quality Assessment
- Confidence Evaluation
- Improvement Recommendations
- Agent Self-Evaluation Tracking

Used By:
- Reflection Engine
- Agent Controller
- Monitoring Layer
- Analytics Dashboard

===========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class ReflectionResult:

    # =====================================================
    # EXECUTION STATUS
    # =====================================================

    passed: bool

    improvement_required: bool

    # =====================================================
    # OVERALL SCORES
    # =====================================================

    quality_score: float

    confidence_score: float

    # =====================================================
    # DETAILED METRICS
    # =====================================================

    length_score: float = 0.0

    educational_score: float = 0.0

    structure_score: float = 0.0

    intent_alignment_score: float = 0.0

    personalization_score: float = 0.0

    safety_score: float = 0.0

    # =====================================================
    # FEEDBACK
    # =====================================================

    feedback: str = ""

    improvement_suggestions: List[str] = field(
        default_factory=list
    )

    reflection_notes: List[str] = field(
        default_factory=list
    )

    # =====================================================
    # METADATA
    # =====================================================

    evaluated_at: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

    evaluator_version: str = "2.0"

    metadata: Dict = field(
        default_factory=dict
    )

    # =====================================================
    # HELPER METHODS
    # =====================================================

    def add_suggestion(
        self,
        suggestion: str
    ):
        """
        Add improvement suggestion.
        """

        self.improvement_suggestions.append(
            suggestion
        )

    def add_note(
        self,
        note: str
    ):
        """
        Add reflection note.
        """

        self.reflection_notes.append(
            note
        )

    def is_high_quality(self) -> bool:
        """
        Check whether response exceeds
        high quality threshold.
        """

        return self.quality_score >= 0.90

    def is_acceptable(self) -> bool:
        """
        Check whether response passes
        minimum quality requirements.
        """

        return self.passed

    def to_dict(self):
        """
        Convert ReflectionResult into dictionary.
        Useful for API responses, logging,
        monitoring and analytics.
        """

        return {

            "passed":
                self.passed,

            "improvement_required":
                self.improvement_required,

            "quality_score":
                self.quality_score,

            "confidence_score":
                self.confidence_score,

            "length_score":
                self.length_score,

            "educational_score":
                self.educational_score,

            "structure_score":
                self.structure_score,

            "intent_alignment_score":
                self.intent_alignment_score,

            "personalization_score":
                self.personalization_score,

            "safety_score":
                self.safety_score,

            "feedback":
                self.feedback,

            "improvement_suggestions":
                self.improvement_suggestions,

            "reflection_notes":
                self.reflection_notes,

            "evaluated_at":
                self.evaluated_at,

            "evaluator_version":
                self.evaluator_version,

            "metadata":
                self.metadata
        }
