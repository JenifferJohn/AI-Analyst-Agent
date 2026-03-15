import re


def validate_user_query(query, df):
    """
    Validate that user query references dataset columns
    """

    try:

        # -------- BASIC VALIDATION --------
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

        if df is None or df.empty:

            return {
                "status": "warning",
                "message": "Dataset is not loaded.",
                "data": None,
                "suggestions": [
                    "Upload a dataset",
                    "Load an Excel file first"
                ]
            }

        query = query.lower()

        # -------- DATASET COLUMN LIST --------
        columns = [c.lower() for c in df.columns]

        # -------- TOKENIZE QUERY --------
        query_words = re.findall(r"\b\w+\b", query)

        # -------- DIRECT COLUMN MATCH --------
        for col in columns:
            if col in query:
                return {
                    "status": "success",
                    "message": None,
                    "data": query,
                    "suggestions": []
                }

        # -------- PARTIAL COLUMN MATCH --------
        for word in query_words:
            for col in columns:
                if word in col:
                    return {
                        "status": "success",
                        "message": None,
                        "data": query,
                        "suggestions": []
                    }

        # -------- NO COLUMN MATCH --------
        sample_columns = columns[:3]

        suggestions = []

        for col in sample_columns:
            suggestions.append(f"Show trend for {col}")

        suggestions.append("Show correlation between variables")

        return {
            "status": "warning",
            "message": "Query does not reference dataset columns.",
            "data": None,
            "suggestions": suggestions
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Query validation failed.",
            "data": None,
            "suggestions": [
                "Ask about sales trends",
                "Ask about product performance"
            ]
        }