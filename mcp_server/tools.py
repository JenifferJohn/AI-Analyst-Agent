import pandas as pd

from analytics.insight_engine import generate_insights
from analytics.root_cause_engine import discover_root_cause
from analytics.chart_selector import choose_chart

# GLOBAL DATAFRAME STORE

DATAFRAME = None


def set_dataframe(df):
    """
    Set dataframe for MCP tools
    """
    global DATAFRAME
    DATAFRAME = df


# DATASET SCHEMA TOOL

def get_schema():
    """
    Return dataset schema metadata
    """

    try:

        if DATAFRAME is None or DATAFRAME.empty:
            return {
                "status": "warning",
                "message": "Dataset not loaded.",
                "data": None,
                "suggestions": [
                    "Upload an Excel dataset first"
                ]
            }

        schema = {
            "columns": list(DATAFRAME.columns),
            "row_count": int(len(DATAFRAME)),
            "column_types": {
                col: str(dtype)
                for col, dtype in DATAFRAME.dtypes.items()
            }
        }

        return {
            "status": "success",
            "message": None,
            "data": schema,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Failed to retrieve dataset schema.",
            "data": None,
            "suggestions": []
        }


# INSIGHT TOOL

def run_insight_tool():
    """
    Generate dataset insights
    """

    try:

        if DATAFRAME is None or DATAFRAME.empty:

            return {
                "status": "warning",
                "message": "Dataset not loaded.",
                "data": None,
                "suggestions": [
                    "Upload an Excel dataset"
                ]
            }

        insights = generate_insights(DATAFRAME)

        return {
            "status": "success",
            "message": None,
            "data": insights,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Insight generation failed.",
            "data": None,
            "suggestions": []
        }


# --------------------------------------------------
# ROOT CAUSE TOOL
# --------------------------------------------------
def run_root_cause_tool(target_column=None):
    """
    Run root cause discovery
    """

    try:

        if DATAFRAME is None or DATAFRAME.empty:

            return {
                "status": "warning",
                "message": "Dataset not loaded.",
                "data": None,
                "suggestions": [
                    "Upload dataset first"
                ]
            }

        result = discover_root_cause(DATAFRAME, target_column)

        return {
            "status": "success",
            "message": None,
            "data": result,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Root cause analysis failed.",
            "data": None,
            "suggestions": []
        }


# --------------------------------------------------
# CHART TOOL
# --------------------------------------------------
def run_chart_tool():
    """
    Generate recommended chart
    """

    try:

        if DATAFRAME is None or DATAFRAME.empty:

            return {
                "status": "warning",
                "message": "Dataset not loaded.",
                "data": None,
                "suggestions": [
                    "Upload dataset first"
                ]
            }

        chart = choose_chart(DATAFRAME)

        return {
            "status": "success",
            "message": None,
            "data": chart,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Chart generation failed.",
            "data": None,
            "suggestions": []
        }