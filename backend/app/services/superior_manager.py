"""
===========================================================
LANGUAGE LEARNING PAL - SUPERIOR MANAGER
Phase 2 - Supervisor -> Superior Manager Refactor

Purpose:
- Central orchestration layer
- Decide how a user request should be handled
- Run Grammar, Vocabulary and Cultural Bridge as first-stage agents
- Merge structured outputs without field collisions
- Provide extension points for Confidence and Audit agents
===========================================================
"""

from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.services.intent_engine import IntentEngine
from app.services.prompt_manager import PromptManager
from app.services.llm_service import generate_response
from app.services.tool_router import ToolRouter
from app.services.cultural_bridge_agent import CulturalBridgeAgent
from app.services.confidence_agent import ConfidenceAgent
from app.services.audit_agent import AuditAgent


class SuperiorManager:

    TOOL_INTENTS = {
        "VOCABULARY",
        "WORD_OF_DAY",
        "SYNONYMS",
        "ANTONYMS",
        "TRANSLATION",
        "PRONUNCIATION",
        "CULTURAL",
    }

    LLM_INTENTS = {
        "GRAMMAR",
        "CONVERSATION",
        "DAILY_PHRASES",
        "CULTURAL_BRIDGE",
    }

    PLANNING_INTENTS = {
        "LEARNING_PLAN",
        "ROADMAP",
        "CURRENT_DAY",
        "PROGRESS",
    }

    # =====================================================
    # EXISTING ROUTING
    # =====================================================

    @classmethod
    def analyze_request(cls, message: str) -> Dict[str, Any]:
        intent_result = IntentEngine.analyze(message)

        intent = intent_result.intent
        confidence = intent_result.confidence

        return {
            "intent": intent,
            "confidence": confidence,
            "route": cls.select_route(intent),
        }

    @classmethod
    def select_route(cls, intent: str) -> str:

        if intent in cls.TOOL_INTENTS:
            return "TOOL"

        if intent in cls.LLM_INTENTS:
            return "LLM"

        if intent in cls.PLANNING_INTENTS:
            return "PLANNING"

        return "GENERAL"

    @classmethod
    def build_strategy(cls, intent: str) -> Dict[str, Any]:

        route = cls.select_route(intent)

        if route == "TOOL":
            return {
                "route": "TOOL",
                "use_tools": True,
                "use_memory": False,
                "use_planning": False,
            }

        if route == "LLM":
            return {
                "route": "LLM",
                "use_tools": False,
                "use_memory": True,
                "use_planning": False,
            }

        if route == "PLANNING":
            return {
                "route": "PLANNING",
                "use_tools": False,
                "use_memory": True,
                "use_planning": True,
            }

        return {
            "route": "GENERAL",
            "use_tools": False,
            "use_memory": True,
            "use_planning": False,
        }

    @classmethod
    def decide(
        cls,
        intent: str,
        confidence: float
    ) -> Dict[str, Any]:

        route = cls.select_route(intent)
        strategy = cls.build_strategy(intent)

        return {
            "intent": intent,
            "confidence": confidence,
            "route": route,
            "strategy": strategy,
        }

    # =====================================================
    # PHASE 2 - FIRST STAGE
    # =====================================================

    @classmethod
    def run_grammar(
        cls,
        message: str,
        memory=None
    ) -> Dict[str, Any]:

        try:
            prompt = PromptManager.build_prompt(
                message=message,
                intent="GRAMMAR",
                memory=memory,
            )

            response = generate_response(prompt)

            return {
                "success": True,
                "response": response,
            }

        except Exception as e:
            return {
                "success": False,
                "response": None,
                "error": str(e),
            }

    @classmethod
    def run_vocabulary(
        cls,
        message: str
    ) -> Dict[str, Any]:

        try:
            result = ToolRouter.execute_tool(
                "VOCABULARY",
                message
            )

            if result is None:
                return {
                    "success": False,
                    "result": None,
                    "error": "Vocabulary tool returned no result.",
                }

            # Convert ToolResult to a JSON-serializable dictionary.
            if hasattr(result, "model_dump"):
                result_data = result.model_dump()
            elif hasattr(result, "dict"):
                result_data = result.dict()
            elif hasattr(result, "__dict__"):
                result_data = vars(result)
            else:
                result_data = str(result)

            return {
                "success": result.success,
                "result": result_data,
                "message": result.message,
            }

        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }

    @classmethod
    def run_cultural(
        cls,
        message: str
    ) -> Dict[str, Any]:

        try:
            result = CulturalBridgeAgent.process(message)

            return {
                "success": True,
                "result": result,
            }

        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }

    @classmethod
    def run_first_stage(
        cls,
        message: str,
        memory=None
    ) -> Dict[str, Any]:
        """
        Run Grammar, Vocabulary and Cultural Bridge
        concurrently as the first orchestration stage.
        """

        outputs = {}

        tasks = {
            "grammar": lambda: cls.run_grammar(
                message,
                memory
            ),
            "vocabulary": lambda: cls.run_vocabulary(
                message
            ),
            "cultural": lambda: cls.run_cultural(
                message
            ),
        }

        with ThreadPoolExecutor(max_workers=3) as executor:

            futures = {
                executor.submit(task): name
                for name, task in tasks.items()
            }

            for future in as_completed(futures):

                name = futures[future]

                try:
                    outputs[name] = future.result()

                except Exception as e:
                    outputs[name] = {
                        "success": False,
                        "result": None,
                        "error": str(e),
                    }

        return cls.merge_stage_outputs(outputs)

    # =====================================================
    # PHASE 2 - STRUCTURED MERGE
    # =====================================================

    @classmethod
    def merge_stage_outputs(
        cls,
        outputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Keep each agent output under its own namespace.

        This prevents field collisions between agents.
        """

        return {
            "grammar": outputs.get("grammar", {}),
            "vocabulary": outputs.get("vocabulary", {}),
            "cultural": outputs.get("cultural", {}),
        }

    @classmethod
    def orchestrate_first_stage(
        cls,
        message: str,
        memory=None
    ) -> Dict[str, Any]:
        """
        Run the first-stage agents and return their merged output.
        This is the main Phase 2 entry point for AgentController.
        """

        first_stage = cls.run_first_stage(
            message=message,
            memory=memory
        )

        agent_successes = [
            result.get("success", False)
            for result in first_stage.values()
        ]

        stage_status = (
            "completed"
            if all(agent_successes)
            else "completed_with_agent_errors"
        )

        return {
            "stage": "FIRST_STAGE",
            "agents": first_stage,
            "status": stage_status
        }

    # =====================================================
    # PHASE 2 - SECOND STAGE AGENTS
    # =====================================================

    @classmethod
    def run_confidence(
        cls,
        message: str
    ) -> Dict[str, Any]:
        """
        Run the Confidence Coach on a text string.
        """

        try:
            result = ConfidenceAgent.process(message)

            return {
                "success": True,
                "result": result,
            }

        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }

    @classmethod
    def run_audit(
        cls,
        text: str
    ) -> Dict[str, Any]:
        """
        Run the Audit Agent on a text string.
        """

        try:
            result = AuditAgent.process(text)

            return {
                "success": True,
                "result": result,
            }

        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }

    # =====================================================
    # PHASE 2 - SECOND STAGE INTERFACE
    # =====================================================

    @classmethod
    def build_second_stage_input(
        cls,
        first_stage_outputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare the merged first-stage output for the
        second-stage Confidence and Audit agents.
        """

        return {
            "grammar": first_stage_outputs.get("grammar", {}),
            "vocabulary": first_stage_outputs.get("vocabulary", {}),
            "cultural": first_stage_outputs.get("cultural", {}),
        }

    @classmethod
    def run_second_stage(
        cls,
        first_stage_outputs: Dict[str, Any],
        confidence_agent=None,
        audit_agent=None
    ) -> Dict[str, Any]:
        """
        Second-stage orchestration interface.

        Confidence runs after first-stage merge.
        Audit runs after Confidence output.
        """

        merged_input = cls.build_second_stage_input(
            first_stage_outputs
        )

        # Extract text for second-stage agents.
        text_for_second_stage = (
            merged_input.get("grammar", {}).get("response", "")
            or merged_input.get("cultural", {}).get(
                "result", {}
            ).get("improved", "")
            or ""
        )

        result = {
            "confidence": None,
            "audit": None,
            "input": merged_input,
            "status": "pending",
        }

        # =================================================
        # CONFIDENCE COACH
        # =================================================

        import time
        confidence_start = time.perf_counter()

        if confidence_agent is not None:
            result["confidence"] = confidence_agent(
                text_for_second_stage
            )

        elif text_for_second_stage:
            result["confidence"] = cls.run_confidence(
                text_for_second_stage
            )
        print(f"[TIMING] Confidence: {time.perf_counter() - confidence_start:.2f}s")
        # =================================================
        # GET IMPROVED TEXT FROM CONFIDENCE AGENT
        # =================================================

        confidence_text = ""

        if result["confidence"]:
            conf_result = result["confidence"]

            if isinstance(conf_result, dict):
                inner = conf_result.get(
                    "result",
                    conf_result
                )

                if isinstance(inner, dict):
                    confidence_text = inner.get(
                        "improved",
                        text_for_second_stage
                    )

        audit_text = (
            confidence_text
            or text_for_second_stage
        )

        # =================================================
        # AUDIT AGENT
        # =================================================

        audit_start = time.perf_counter()

        if audit_agent is not None:
            result["audit"] = audit_agent(
                audit_text
            )

        elif audit_text:
            result["audit"] = cls.run_audit(
                audit_text
            )
        print(f"[TIMING] Audit: {time.perf_counter() - audit_start:.2f}s")
        # =================================================
        # FINAL STATUS
        # =================================================

        if result["confidence"] and result["audit"]:
            result["status"] = "completed"

        return result

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    @classmethod
    def health_check(cls):

        return {
            "status": "healthy",
            "manager": "SuperiorManager",
            "phase": "Phase 2",
            "routes": [
                "TOOL",
                "LLM",
                "PLANNING",
                "GENERAL",
            ],
            "first_stage_agents": [
                "Grammar",
                "Vocabulary",
                "Cultural Bridge",
            ],
            "second_stage_agents": [
                "Confidence",
                "Audit",
            ],
        }