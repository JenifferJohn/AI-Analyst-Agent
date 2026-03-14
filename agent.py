def analyze_question(question, df):

    rows = df.shape[0]
    cols = df.shape[1]

    response = f"""
Dataset contains {rows} rows and {cols} columns.

Question asked:
{question}

This MVP currently returns basic dataset insights.
"""

    return response