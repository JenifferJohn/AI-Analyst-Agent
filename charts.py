import plotly.express as px

def generate_chart(df):

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) >= 2:

        x = numeric_cols[0]
        y = numeric_cols[1]

        fig = px.scatter(df, x=x, y=y)

        return fig

    else:

        fig = px.histogram(df, x=numeric_cols[0])

        return fig