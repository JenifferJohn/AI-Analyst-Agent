def build_safe_context(df, insights, root_cause):
    """
    Build safe context for LLM analysis
    """

    try:

        # -------- DATASET VALIDATION --------
        if df is None or df.empty:

            return {
                "status": "warning",
                "message": "Dataset is empty.",
                "data": None,
                "suggestions": [
                    "Upload a dataset",
                    "Check file loading"
                ]
            }

        # -------- SCHEMA INFORMATION --------
        schema = {
            "columns": list(df.columns),
            "row_count": int(len(df)),
            "column_types": {
                col: str(dtype)
                for col, dtype in df.dtypes.items()
            }
        }

        # -------- SAMPLE DATA (LIMITED) --------
        sample_rows = df.head(5).to_dict(orient="records")

        # -------- NUMERIC SUMMARY --------
        numeric_cols = df.select_dtypes(include="number").columns

        numeric_summary = {}

        if len(numeric_cols) > 0:

            desc = df[numeric_cols].describe().to_dict()

            numeric_summary = desc

        # -------- CONTEXT OBJECT --------
        context = {
            "schema": schema,
            "sample_rows": sample_rows,
            "numeric_summary": numeric_summary,
            "insights": insights if insights else [],
            "root_cause": root_cause if root_cause else {}
        }

        return {
            "status": "success",
            "message": None,
            "data": context,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Context construction failed.",
            "data": None,
            "suggestions": [
                "Try reloading the dataset",
                "Check dataset format"
            ]
        }