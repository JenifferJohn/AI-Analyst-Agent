import pandas as pd


def load_excel(file):
    """
    Safely load Excel file into pandas dataframe
    """

    try:

        if file is None:

            return {
                "status": "warning",
                "message": "No file uploaded.",
                "data": None,
                "suggestions": ["Upload an Excel file"]
            }

        df = pd.read_excel(file)

        if df.empty:

            return {
                "status": "warning",
                "message": "Excel file contains no data.",
                "data": None,
                "suggestions": ["Check file content"]
            }

        return {
            "status": "success",
            "message": None,
            "data": df,
            "suggestions": []
        }

    except Exception as e:

        return {
            "status": "warning",
            "message": f"Error loading Excel file: {str(e)}",
            "data": None,
            "suggestions": [
                "Upload a valid Excel file (.xlsx)",
                "Check file format"
            ]
        }


def clean_dataframe(df):
    """
    Basic dataframe cleaning
    """

    try:

        if df is None or df.empty:
            return df

        # -------- REMOVE EMPTY COLUMNS --------
        df = df.dropna(axis=1, how="all")

        # -------- REMOVE DUPLICATE ROWS --------
        df = df.drop_duplicates()

        # -------- TRIM COLUMN NAMES --------
        df.columns = df.columns.str.strip()

        # -------- STANDARDIZE COLUMN NAMES --------
        df.columns = df.columns.str.replace(" ", "_").str.lower()

        # -------- TRY CONVERTING NUMERIC COLUMNS --------
        for col in df.columns:

            if df[col].dtype == "object":

                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    pass

        return df

    except Exception:

        return df


def detect_schema(df):
    """
    Detect dataset schema types
    """

    try:

        if df is None or df.empty:
            return {}

        schema = {}

        for col in df.columns:

            dtype = df[col].dtype

            if pd.api.types.is_numeric_dtype(dtype):

                schema[col] = "numeric"

            elif pd.api.types.is_datetime64_any_dtype(dtype):

                schema[col] = "datetime"

            else:

                schema[col] = "categorical"

        return schema

    except Exception:

        return {}