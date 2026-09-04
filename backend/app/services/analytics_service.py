"""
===========================================================
LANGUAGE LEARNING PAL ANALYTICS SERVICE
Version: 2.0

Purpose:
- Agent Monitoring
- Usage Analytics
- Performance Tracking
- Quality Tracking
- Error Tracking
- Dashboard Metrics

===========================================================
"""

import json

from pathlib import Path
from collections import Counter
from datetime import datetime


class AnalyticsService:

    ANALYTICS_FILE = Path(
        "app/storage/analytics.json"
    )

    # =====================================================
    # STORAGE LAYER
    # =====================================================

    @classmethod
    def initialize(cls):

        if not cls.ANALYTICS_FILE.exists():

            cls.ANALYTICS_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            default_data = {

                "total_requests": 0,

                "successful_requests": 0,

                "failed_requests": 0,

                "average_response_time": 0,

                "average_quality_score": 0,

                "intents": [],

                "tools": [],

                "errors": [],

                "daily_usage": {}
            }

            cls.save(default_data)

    @classmethod
    def load(cls):

        cls.initialize()

        try:

            with open(
                cls.ANALYTICS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:

            return {}

    @classmethod
    def save(cls, data):

        with open(
            cls.ANALYTICS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =====================================================
    # REQUEST TRACKING
    # =====================================================

    @classmethod
    def track_request(cls):

        data = cls.load()

        data["total_requests"] += 1

        today = datetime.utcnow().strftime(
            "%Y-%m-%d"
        )

        daily_usage = data.get(
            "daily_usage",
            {}
        )

        daily_usage[today] = (
            daily_usage.get(today, 0) + 1
        )

        data["daily_usage"] = daily_usage

        cls.save(data)

    @classmethod
    def track_success(cls):

        data = cls.load()

        data["successful_requests"] += 1

        cls.save(data)

    @classmethod
    def track_failure(cls):

        data = cls.load()

        data["failed_requests"] += 1

        cls.save(data)

    # =====================================================
    # INTENT TRACKING
    # =====================================================

    @classmethod
    def track_intent(
        cls,
        intent: str
    ):

        data = cls.load()

        data["intents"].append(
            intent
        )

        cls.save(data)

    # =====================================================
    # TOOL TRACKING
    # =====================================================

    @classmethod
    def track_tool(
        cls,
        tool_name: str
    ):

        data = cls.load()

        data["tools"].append(
            tool_name
        )

        cls.save(data)

    # =====================================================
    # ERROR TRACKING
    # =====================================================

    @classmethod
    def track_error(
        cls,
        error_code: str
    ):

        data = cls.load()

        data["errors"].append({

            "error_code":
                error_code,

            "timestamp":
                datetime.utcnow()
                .isoformat()
        })

        cls.save(data)

    # =====================================================
    # QUALITY TRACKING
    # =====================================================

    @classmethod
    def track_quality_score(
        cls,
        score: float
    ):

        data = cls.load()

        current_avg = data.get(
            "average_quality_score",
            0
        )

        total_requests = max(
            1,
            data.get(
                "successful_requests",
                1
            )
        )

        new_avg = (

            (
                current_avg
                * (total_requests - 1)
            )

            + score

        ) / total_requests

        data["average_quality_score"] = round(
            new_avg,
            2
        )

        cls.save(data)

    # =====================================================
    # PERFORMANCE TRACKING
    # =====================================================

    @classmethod
    def track_response_time(
        cls,
        response_time: float
    ):

        data = cls.load()

        current_avg = data.get(
            "average_response_time",
            0
        )

        total_requests = max(
            1,
            data.get(
                "successful_requests",
                1
            )
        )

        new_avg = (

            (
                current_avg
                * (total_requests - 1)
            )

            + response_time

        ) / total_requests

        data["average_response_time"] = round(
            new_avg,
            3
        )

        cls.save(data)

    # =====================================================
    # DASHBOARD
    # =====================================================

    @classmethod
    def get_dashboard(cls):

        data = cls.load()

        intent_counter = Counter(
            data.get(
                "intents",
                []
            )
        )

        tool_counter = Counter(
            data.get(
                "tools",
                []
            )
        )

        success = data.get(
            "successful_requests",
            0
        )

        total = data.get(
            "total_requests",
            0
        )

        success_rate = 0

        if total > 0:

            success_rate = round(
                (success / total) * 100,
                2
            )

        return {

            "total_requests":
                total,

            "successful_requests":
                success,

            "failed_requests":
                data.get(
                    "failed_requests",
                    0
                ),

            "success_rate":
                success_rate,

            "average_response_time":
                data.get(
                    "average_response_time",
                    0
                ),

            "average_quality_score":
                data.get(
                    "average_quality_score",
                    0
                ),

            "most_used_intent":

                intent_counter
                .most_common(1)[0][0]

                if intent_counter
                else None,

            "most_used_tool":

                tool_counter
                .most_common(1)[0][0]

                if tool_counter
                else None,

            "daily_usage":
                data.get(
                    "daily_usage",
                    {}
                )
        }

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    @classmethod
    def health_check(cls):

        dashboard = cls.get_dashboard()

        return {

            "status": "healthy",

            "analytics_enabled": True,

            "total_requests":
                dashboard["total_requests"],

            "success_rate":
                dashboard["success_rate"]
        }

    # =====================================================
    # RESET ANALYTICS
    # =====================================================

    @classmethod
    def reset(cls):

        if cls.ANALYTICS_FILE.exists():

            cls.ANALYTICS_FILE.unlink()

        cls.initialize()
