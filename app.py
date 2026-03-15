import streamlit as st
import pandas as pd

from analytics.analysis_pipeline import run_analysis
from agents.persona_router import route_persona
from semantic_layer.business_mapper import map_business_terms
from agents.clarification_agent import clarify_question
from guardrails.guardrail_controller import (
    run_input_guardrail,
    run_context_guardrail,
    run_output_guardrail
)

st.set_page_config(page_title="AI Excel Analyst", layout="wide")

st.title("AI Excel Analyst")

profile = st.selectbox(
    "User Profile",
    ["Non-technical Manager", "Technical Manager"]
)

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:

    try:
        df = pd.read_excel(uploaded_file)
    except Exception:
        st.error("Unable to read Excel file.")
        st.stop()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    query = st.chat_input("Ask a question about your dataset")

    if query:

        query = map_business_terms(query)

        input_result = run_input_guardrail(query, df)

        if input_result["status"] != "success":

            st.warning(input_result["message"])

            for s in input_result["suggestions"]:
                st.button(s)

        else:

            clarification = clarify_question(query, df)

            if clarification:

                st.warning(clarification)

                for col in df.columns[:5]:

                    if st.button(f"Analyze {col}"):

                        query = f"Analyze {col}"

            else:

                analysis = run_analysis(df)

                if analysis["status"] != "success":

                    st.warning(analysis["message"])

                else:

                    insights = analysis["data"]["insights"]
                    root_cause = analysis["data"]["root_cause"]
                    chart = analysis["data"]["chart"]

                    context = run_context_guardrail(
                        df,
                        insights,
                        root_cause
                    )["data"]

                    persona_result = route_persona(
                        profile,
                        query,
                        context
                    )

                    output_result = run_output_guardrail(
                        persona_result["data"],
                        df
                    )

                    if output_result["status"] != "success":

                        st.warning(output_result["message"])

                    else:

                        col1, col2 = st.columns(2)

                        with col1:

                            st.subheader("Insights")

                            for i in insights:
                                st.write("-", i)

                            st.subheader("Root Cause Drivers")

                            st.json(root_cause)

                        with col2:

                            if chart:
                                st.plotly_chart(chart)

                        st.subheader("AI Explanation")

                        st.write(output_result["data"])