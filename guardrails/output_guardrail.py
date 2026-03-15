import re


def validate_output(response, df):
    """
    Validate LLM response against dataframe schema and dataset values.
    """

    try:

        # -------- EMPTY RESPONSE CHECK --------
        if not response or len(response.strip()) == 0:

            return {
                "status": "warning",
                "message": "AI returned empty response.",
                "data": None,
                "suggestions": [
                    "Ask about sales trends",
                    "Ask which product performs best"
                ]
            }

        response_lower = response.lower()

        # -------- DATASET COLUMN LIST --------
        columns = [c.lower() for c in df.columns]

        # -------- COLUMN HALLUCINATION CHECK --------
        extracted_words = re.findall(r"\b[a-zA-Z_]+\b", response_lower)

        invalid_columns = [
            word for word in extracted_words
            if word.endswith("_column") and word not in columns
        ]

        if invalid_columns:

            return {
                "status": "warning",
                "message": f"Response references unknown columns: {invalid_columns}",
                "data": None,
                "suggestions": [
                    "Ask about available dataset columns",
                    f"Try asking about {columns[0]}"
                ]
            }

        # -------- HALLUCINATION KEYWORDS --------
        forbidden_terms = [
            "training data",
            "internet",
            "openai",
            "chatgpt",
            "language model"
        ]

        for term in forbidden_terms:

            if term in response_lower:

                return {
                    "status": "warning",
                    "message": "Response contains irrelevant hallucinated information.",
                    "data": None,
                    "suggestions": [
                        "Ask about dataset insights",
                        "Ask about trends in the data"
                    ]
                }

        # -------- NUMBER VALIDATION --------
        numeric_cols = df.select_dtypes(include="number").columns

        numbers_in_dataset = set()

        for col in numeric_cols:

            numbers_in_dataset.update(
                df[col].dropna().astype(str).tolist()
            )

        numbers_in_response = re.findall(r"\b\d+\.?\d*\b", response_lower)

        hallucinated_numbers = []

        for num in numbers_in_response:

            if num not in numbers_in_dataset:
                hallucinated_numbers.append(num)

        # Allow small number of mismatches (percentages / rounding)
        if len(hallucinated_numbers) > 2:

            return {
                "status": "warning",
                "message": "Possible hallucinated numbers detected in AI response.",
                "data": response,
                "suggestions": [
                    "Ask for explanation of calculations",
                    "Ask which dataset values were used"
                ]
            }

        # -------- SUCCESS --------
        return {
            "status": "success",
            "message": None,
            "data": response,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Output validation failed.",
            "data": response,
            "suggestions": [
                "Try asking a simpler question",
                "Ask about dataset trends"
            ]
        }