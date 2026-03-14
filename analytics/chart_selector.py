from langchain_community.llms import Ollama
import plotly.express as px

llm = Ollama(model="llama3")


def choose_chart(df):
    """
    LLM decides best chart type for dataset
    """

    columns = list(df.columns)

    prompt = f"""
Dataset columns:
{columns}

Choose best visualization type for general exploration.

Return ONLY one word from:
bar
line
scatter
histogram
"""

    chart_type = llm.invoke(prompt).strip().lower()

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        return None

    # scatter chart
    if chart_type == "scatter" and len(numeric_cols) >= 2:

        return px.scatter(
            df,
            x=numeric_cols[0],
            y=numeric_cols[1],
            title="Scatter Relationship"
        )

    # line chart
    if chart_type == "line":

        return px.line(
            df,
            y=numeric_cols[0],
            title="Trend Analysis"
        )

    # bar chart
    if chart_type == "bar":

        return px.bar(
            df,
            x=df.columns[0],
            y=numeric_cols[0],
            title="Category Comparison"
        )

    # histogram fallback
    return px.histogram(
        df,
        x=numeric_cols[0],
        title="Distribution"
    )