import streamlit as st
import pandas as pd
from data_profiler import profile_data
from charts import generate_chart
from report_generator import export_report
from agent import analyze_question

st.title("AI BI Analyst")

uploaded_file = st.file_uploader("Upload Excel Dataset")

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Profile")
    profile = profile_data(df)

    st.write(profile)

    question = st.text_input("Ask a business question")

    if question:

        response = analyze_question(question, df)

        st.subheader("Insight")
        st.write(response)

    st.subheader("Chart")

    fig = generate_chart(df)

    st.plotly_chart(fig)

    if st.button("Export Report"):

        export_report(df)

        st.success("Report exported to exports folder")