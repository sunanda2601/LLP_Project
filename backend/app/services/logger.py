"""
===========================================================
LANGUAGE LEARNING PAL LOGGER
Version: 2.0

Purpose:
- Centralized Logging
- Audit Trail
- Error Tracking
- Performance Monitoring
- Agent Execution Tracking

===========================================================
"""

import json
import logging

from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


class AgentLogger:

    _initialized = False

    logger = logging.getLogger("LanguageLearningPal")

    LOG_DIRECTORY = Path("logs")

    LOG_FILE = LOG_DIRECTORY / "agent.log"

    ERROR_FILE = LOG_DIRECTORY / "errors.log"

    AUDIT_FILE = LOG_DIRECTORY / "audit.log"

    # =====================================================
    # INITIALIZATION
    # =====================================================

    @classmethod
    def initialize(cls):

        if cls._initialized:
            return

        cls.LOG_DIRECTORY.mkdir(
            exist_ok=True
        )

        cls.logger.setLevel(
            logging.INFO
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        # ===============================================
        # MAIN LOG FILE
        # ===============================================

        main_handler = RotatingFileHandler(

            cls.LOG_FILE,

            maxBytes=5 * 1024 * 1024,

            backupCount=5,

            encoding="utf-8"
        )

        main_handler.setFormatter(
            formatter
        )

        # ===============================================
        # ERROR LOG FILE
        # ===============================================

        error_handler = RotatingFileHandler(

            cls.ERROR_FILE,

            maxBytes=5 * 1024 * 1024,

            backupCount=5,

            encoding="utf-8"
        )

        error_handler.setLevel(
            logging.ERROR
        )

        error_handler.setFormatter(
            formatter
        )

        # ===============================================
        # CONSOLE LOGGING
        # ===============================================

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(
            formatter
        )

        cls.logger.addHandler(
            main_handler
        )

        cls.logger.addHandler(
            error_handler
        )

        cls.logger.addHandler(
            console_handler
        )

        cls._initialized = True

    # =====================================================
    # INFO
    # =====================================================

    @classmethod
    def info(cls, message: str):

        cls.initialize()

        cls.logger.info(message)

    # =====================================================
    # WARNING
    # =====================================================

    @classmethod
    def warning(cls, message: str):

        cls.initialize()

        cls.logger.warning(message)

    # =====================================================
    # ERROR
    # =====================================================

    @classmethod
    def error(cls, message: str):

        cls.initialize()

        cls.logger.error(message)

    # =====================================================
    # CRITICAL
    # =====================================================

    @classmethod
    def critical(cls, message: str):

        cls.initialize()

        cls.logger.critical(message)

    # =====================================================
    # AGENT EXECUTION LOG
    # =====================================================

    @classmethod
    def log_agent_execution(

        cls,

        session_id: str,

        user_id: str,

        intent: str,

        state: str
    ):

        cls.initialize()

        cls.logger.info(

            f"[AGENT] "

            f"Session={session_id} | "

            f"User={user_id} | "

            f"Intent={intent} | "

            f"State={state}"
        )

    # =====================================================
    # TOOL EXECUTION LOG
    # =====================================================

    @classmethod
    def log_tool_execution(

        cls,

        tool_name: str,

        success: bool
    ):

        cls.initialize()

        cls.logger.info(

            f"[TOOL] "

            f"{tool_name} | "

            f"Success={success}"
        )

    # =====================================================
    # MEMORY LOG
    # =====================================================

    @classmethod
    def log_memory_event(

        cls,

        user_id: str,

        event: str
    ):

        cls.initialize()

        cls.logger.info(

            f"[MEMORY] "

            f"User={user_id} | "

            f"Event={event}"
        )

    # =====================================================
    # REFLECTION LOG
    # =====================================================

    @classmethod
    def log_reflection(

        cls,

        quality_score: float,

        passed: bool
    ):

        cls.initialize()

        cls.logger.info(

            f"[REFLECTION] "

            f"Score={quality_score} | "

            f"Passed={passed}"
        )

    # =====================================================
    # PERFORMANCE LOG
    # =====================================================

    @classmethod
    def log_performance(

        cls,

        operation: str,

        execution_time: float
    ):

        cls.initialize()

        cls.logger.info(

            f"[PERFORMANCE] "

            f"{operation} | "

            f"{execution_time:.3f}s"
        )

    # =====================================================
    # AUDIT LOG
    # =====================================================

    @classmethod
    def audit(

        cls,

        event_type: str,

        data: dict
    ):

        cls.LOG_DIRECTORY.mkdir(
            exist_ok=True
        )

        payload = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "event_type":
                event_type,

            "data":
                data
        }

        with open(

            cls.AUDIT_FILE,

            "a",

            encoding="utf-8"

        ) as file:

            file.write(
                json.dumps(payload)
            )

            file.write("\n")

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    @classmethod
    def health_check(cls):

        return {

            "status": "healthy",

            "logger": "LanguageLearningPal",

            "log_directory":
                str(cls.LOG_DIRECTORY)
        }
