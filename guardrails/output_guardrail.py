def validate_output(response, df):
    """
    Validate that numbers mentioned in response exist in dataset
    """

    numbers_in_dataset = set()

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:

        numbers_in_dataset.update(
            df[col].astype(str).tolist()
        )

    words = response.split()

    for word in words:

        cleaned = word.replace(".", "", 1)

        if cleaned.isdigit():

            if word not in numbers_in_dataset:

                return False, "Possible hallucinated number detected."

    return True, None