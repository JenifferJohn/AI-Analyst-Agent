import pandas as pd

from analytics.insight_engine import generate_insights
from analytics.root_cause_engine import discover_root_cause
from analytics.chart_selector import choose_chart

# global dataframe
DATAFRAME = None


def set_dataframe(df):
    """
    Set dataframe for MCP tools
    """
    global DATAFRAME
    DATAFRAME = df


def get_schema():
    """
    Return dataset schema
    """

    if DATAFRAME is None:
        return {"error": "Dataset not loaded"}

    return list(DATAFRAME.columns)


def run_insight_tool():
    """
    Generate dataset insights
    """

    if DATAFRAME is None:
        return {"error": "Dataset not loaded"}

    insights = generate_insights(DATAFRAME)

    return insights


def run_root_cause_tool(target_column=None):
    """
    Run root cause discovery
    """

    if DATAFRAME is None:
        return {"error": "Dataset not loaded"}

    root_cause = discover_root_cause(
        DATAFRAME,
        target_column
    )

    return root_cause


def run_chart_tool():
    """
    Generate chart automatically
    """

    if DATAFRAME is None:
        return None

    chart = choose_chart(DATAFRAME)

    return chart