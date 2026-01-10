from tools.llm import call_llm

def email_node(state: dict) -> dict:
    company = state["company"]
    research = state["research_summary"]
    rag_context = state.get("rag_context", "")

    prompt = f"""
Write a single-paragraph B2B cold outreach email body.

STRICT RULES:
- No subject line
- No bullet points
- No markdown
- No headings
- No placeholders
- No greetings like Hi / Hello
- Write plain English prose only
- 6 to 8 complete sentences
- 70 to 120 words total
- Each sentence must be complete and meaningful

Context about the company:
{research}

Client rules:
{rag_context}

Return ONLY the email body text.
"""

    email = call_llm(prompt)

    # hard cleanup
    email = (
        email.replace("Subject:", "")
        .replace("*", "")
        .replace(":", "")
        .strip()
    )

    state["email_draft"] = email
    return state
