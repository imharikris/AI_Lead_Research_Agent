import streamlit as st
from agent.graph import build_agent_graph

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Lead Research Agent",
    page_icon="🤖",
    layout="centered",
)

# ---------------- Global CSS (Typography Control) ----------------
st.markdown(
    """
    <style>
    /* Page title */
    h1 {
        font-size: 32px !important;
        font-weight: 700 !important;
        margin-bottom: 8px !important;
    }

    /* Section headers */
    h2 {
        font-size: 22px !important;
        font-weight: 600 !important;
        margin-top: 24px !important;
        margin-bottom: 8px !important;
    }

    /* Body text */
    p, div, span, li {
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    /* Input labels */
    label {
        font-size: 15px !important;
        font-weight: 500 !important;
    }

    /* Buttons */
    button {
        font-size: 15px !important;
        padding: 8px 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Header ----------------
st.title("🤖 AI Lead Research Agent")
st.markdown(
    "Automated **company research** and **personalized outreach** using an agentic AI system."
)

st.divider()

# ---------------- Input Section ----------------
company_name = st.text_input(
    "Company name",
    placeholder="e.g. Notion, Stripe, Nvidia",
)

run = st.button("🚀 Run Research & Outreach")

# ---------------- Execution ----------------
if run and company_name:
    with st.spinner("Agent is researching the company and drafting outreach..."):
        graph = build_agent_graph()
        result = graph.invoke({"company": company_name})

    st.success("Completed")

    # ---------------- Research Summary ----------------
    st.subheader("🔍 Research Summary")
    st.write(result.get("research_summary", "No summary available."))

    # ---------------- Email Draft ----------------
    st.subheader("✉️ Email Draft")
    email = result.get("email_draft", "No email draft available.")

    # Email rendering (WRAPS PROPERLY, NO HORIZONTAL SCROLL)
    st.markdown(
        f"""
        <div style="
            padding:16px;
            border:1px solid #d0d0d0;
            border-radius:8px;
            background-color:#f9f9f9;
            color:#111;
            white-space: normal;
            word-wrap: break-word;
            overflow-wrap: break-word;
            line-height:1.6;
        ">
        {email}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- Sources ----------------
    st.subheader("🔗 Sources")
    sources = result.get("sources", [])

    if sources:
        for src in sources:
            st.markdown(f"- {src}")
    else:
        st.write("No sources available.")

# ---------------- Footer ----------------
st.divider()
st.caption(
    "Demo showcasing an agentic AI system with planning, web research, "
    "RAG grounding, validation, and persistence."
)
