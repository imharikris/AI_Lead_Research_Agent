import streamlit as st
from agent.graph import build_agent_graph

st.title("AI Lead Research Agent")
company_name = st.text_input("Enter the company name:")
if st.button("Run company research") and company_name:
    graph = build_agent_graph()
    result =graph.invoke({"company": company_name})
    st.subheader("Research Summary:")
    st.write(result.get("research_summary", "No summary available."))
    st.subheader("Email Draft:")
    st.write(result.get("email_draft", "No email draft available."))