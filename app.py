import streamlit as st
import pandas as pd

from core.pipeline import run_ai_pipeline

st.set_page_config(page_title="AI Analyst")

st.title("AI Analyst")

persona = st.selectbox(
    "Select User Type",
    ["Non-technical Manager", "Technical Manager"]
)

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:

    try:
        df = pd.read_excel(uploaded_file)
    except:
        st.error("Unable to read Excel file")
        st.stop()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    query = st.chat_input("Ask a question about the dataset")

    if query:

        result = run_ai_pipeline(query, df, persona)

        if result["status"] != "success":
            st.warning(result["message"])

            if result["suggestions"]:
                st.write("Try these:")
                for s in result["suggestions"]:
                    st.write("-", s)

        if result["insights"]:
            st.subheader("Insights")
            for i in result["insights"]:
                st.write("-", i)

        if result["root_cause"]:
            st.subheader("Root Cause Drivers")
            st.json(result["root_cause"])

        if result["chart"]:
            st.plotly_chart(result["chart"])

        if result["response"]:
            st.subheader("AI Explanation")
            st.write(result["response"])