def profile_data(df):

    profile = {}

    profile["rows"] = df.shape[0]
    profile["columns"] = df.shape[1]
    profile["column_names"] = list(df.columns)

    profile["numeric_columns"] = df.select_dtypes(include="number").columns.tolist()

    profile["categorical_columns"] = df.select_dtypes(include="object").columns.tolist()

    return profile