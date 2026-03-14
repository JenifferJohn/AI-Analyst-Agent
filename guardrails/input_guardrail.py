def validate_user_query(query, df):
    """
    Validate that query references dataset columns
    """

    columns = [c.lower() for c in df.columns]

    query_words = query.lower().split()

    for word in query_words:

        if word in columns:
            return True, None

    return False, "Query does not reference valid dataset columns."