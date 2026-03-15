from langchain_community.llms import Ollama
import plotly.express as px
import pandas as pd

llm = Ollama(model="llama3")


def choose_chart(df):
    """
    Automatically choose a meaningful business chart
    """

    try:

        if df is None or df.empty:
            return None

        columns = list(df.columns)

        numeric_cols = df.select_dtypes(include="number").columns
        categorical_cols = df.select_dtypes(include="object").columns

        # -------- LLM CHART DECISION --------
        prompt = f"""
Dataset columns:
{columns}

Choose the BEST visualization for business insight.

Return ONLY one word from:

bar
line
scatter
histogram
box
heatmap
pie
"""

        try:
            chart_type = llm.invoke(prompt).strip().lower()
        except Exception:
            chart_type = None

        # -------- HEATMAP (correlation insight) --------
        if chart_type == "heatmap" and len(numeric_cols) >= 2:

            corr = df[numeric_cols].corr()

            return px.imshow(
                corr,
                text_auto=True,
                title="Correlation Heatmap"
            )

        # -------- SCATTER (relationship analysis) --------
        if chart_type == "scatter" and len(numeric_cols) >= 2:

            return px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title="Relationship Analysis"
            )

        # -------- LINE (trend insight) --------
        if chart_type == "line" and len(numeric_cols) >= 1:

            return px.line(
                df,
                y=numeric_cols[0],
                title="Trend Analysis"
            )

        # -------- BAR (category comparison) --------
        if chart_type == "bar" and len(categorical_cols) >= 1 and len(numeric_cols) >= 1:

            return px.bar(
                df,
                x=categorical_cols[0],
                y=numeric_cols[0],
                title="Category Performance"
            )

        # -------- PIE (share distribution) --------
        if chart_type == "pie" and len(categorical_cols) >= 1:

            value_counts = df[categorical_cols[0]].value_counts()

            return px.pie(
                values=value_counts.values,
                names=value_counts.index,
                title="Category Share"
            )

        # -------- BOX (outlier detection) --------
        if chart_type == "box" and len(numeric_cols) >= 1:

            return px.box(
                df,
                y=numeric_cols[0],
                title="Outlier Detection"
            )

        # -------- HISTOGRAM (distribution insight) --------
        if chart_type == "histogram" and len(numeric_cols) >= 1:

            return px.histogram(
                df,
                x=numeric_cols[0],
                title="Distribution"
            )

        # -------- RULE-BASED FALLBACKS --------

        # scatter if multiple numeric columns
        if len(numeric_cols) >= 2:

            return px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title="Relationship Analysis"
            )

        # histogram if single numeric
        if len(numeric_cols) == 1:

            return px.histogram(
                df,
                x=numeric_cols[0],
                title="Distribution"
            )

        # bar if categorical exists
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:

            return px.bar(
                df,
                x=categorical_cols[0],
                y=numeric_cols[0],
                title="Category Comparison"
            )

        return None

    except Exception:
        return None