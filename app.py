import streamlit as st
import pandas as pd

from core.pipeline import run_ai_pipeline

st.set_page_config(page_title="AI Analyst")

st.title("AI Analyst")

persona = st.selectbox(
    "User Type",
    ["Non-technical Manager", "Technical Manager"]
)

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

if uploaded_file:

    try:
        df = pd.read_excel(uploaded_file)
    except:
        st.error("Could not read Excel file")
        st.stop()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.write("Quick actions")

    c1, c2, c3 = st.columns(3)

    if c1.button("Generate Insights"):
        query = "What insights exist in this dataset?"

    elif c2.button("Show Trends"):
        query = "Show trends in the dataset"

    elif c3.button("Find Root Causes"):
        query = "What factors influence performance?"

    else:
        query = st.chat_input("Ask a question about your data")

    if query:

        result = run_ai_pipeline(query, df, persona)

        if result["message"]:
            st.warning(result["message"])

        if result["insights"]:
            st.subheader("Insights")

            for i in result["insights"]:
                st.write("-", i)

        if result["root_cause"]:
            st.subheader("Root Cause Drivers")
            st.json(result["root_cause"])

        if result["chart"]:
            st.subheader("Visualization")
            st.plotly_chart(result["chart"])

        if result["response"]:
            st.subheader("AI Explanation")
            st.write(result["response"])

    st.write("Suggested Questions")

    suggestions = [
        "What insights exist in the dataset?",
        "Show sales trend",
        "What drives sales performance?",
        "Explain dataset patterns"
    ]

    for s in suggestions:
        if st.button(s):
            run_ai_pipeline(s, df, persona)