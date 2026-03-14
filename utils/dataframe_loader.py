import pandas as pd


def load_excel(file):
    """
    Safely load Excel file into pandas dataframe
    """

    try:

        df = pd.read_excel(file)

        return df

    except Exception as e:

        raise ValueError(f"Error loading Excel file: {str(e)}")


def clean_dataframe(df):
    """
    Basic dataframe cleaning
    """

    # remove empty columns
    df = df.dropna(axis=1, how="all")

    # remove duplicate rows
    df = df.drop_duplicates()

    return df


def detect_schema(df):
    """
    Detect dataset schema types
    """

    schema = {}

    for col in df.columns:

        dtype = str(df[col].dtype)

        if "int" in dtype or "float" in dtype:
            schema[col] = "numeric"

        elif "datetime" in dtype:
            schema[col] = "datetime"

        else:
            schema[col] = "categorical"

    return schema