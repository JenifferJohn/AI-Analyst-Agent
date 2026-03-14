def build_safe_context(df, insights, root_cause):
    """
    Construct safe context for LLM
    """

    schema = list(df.columns)

    context = {
        "schema": schema,
        "insights": insights,
        "root_cause": root_cause
    }

    return context