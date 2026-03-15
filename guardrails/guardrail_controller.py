import re

from guardrails.input_guardrail import validate_user_query
from guardrails.context_guardrail import build_safe_context
from guardrails.output_guardrail import validate_output


# -------- INPUT GUARDRAIL --------
def run_input_guardrail(query, df):
    """
    Run full query validation pipeline
    """

    try:

        # -------- BASIC CHECK --------
        if not query or len(query.strip()) == 0:
            return {
                "status": "warning",
                "message": "Query cannot be empty.",
                "data": None,
                "suggestions": [
                    "Show sales trend",
                    "Show top products by sales"
                ]
            }

        query = query.lower()

        # -------- PROMPT INJECTION PROTECTION --------
        blocked_patterns = [
            "ignore previous instructions",
            "system prompt",
            "act as",
            "execute code",
            "run shell",
            "import os",
            "delete file",
            "drop table",
            "shutdown",
            "rm -rf"
        ]

        for pattern in blocked_patterns:

            if re.search(pattern, query):

                return {
                    "status": "warning",
                    "message": "Unsafe query detected.",
                    "data": None,
                    "suggestions": [
                        "Ask about dataset trends",
                        "Ask about product performance"
                    ]
                }

        # -------- LENGTH CHECK --------
        if len(query) > 500:

            return {
                "status": "warning",
                "message": "Query is too long.",
                "data": None,
                "suggestions": [
                    "Ask a shorter question",
                    "Focus on one metric"
                ]
            }

        # -------- COLUMN VALIDATION --------
        return validate_user_query(query, df)

    except Exception:

        return {
            "status": "warning",
            "message": "Input validation failed.",
            "data": None,
            "suggestions": [
                "Ask about sales trends",
                "Ask about market performance"
            ]
        }


# -------- CONTEXT GUARDRAIL --------
def run_context_guardrail(df, insights, root_cause):
    """
    Build safe context for LLM
    """

    try:

        return build_safe_context(df, insights, root_cause)

    except Exception:

        return {
            "dataset_schema": {},
            "sample_rows": [],
            "insights": insights if insights else [],
            "root_cause": root_cause if root_cause else {}
        }


# -------- OUTPUT GUARDRAIL --------
def run_output_guardrail(response, df):
    """
    Validate LLM output
    """

    return validate_output(response, df)