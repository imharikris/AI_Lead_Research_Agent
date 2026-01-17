from tools.llm import call_llm

def email_node(state: dict) -> dict:
    company = state["company"]
    research = state["research_summary"]
    rag_context = state.get("rag_context", "")

    prompt = f"""
You are an SDR writing a cold outreach email TO a decision-maker at the company below.

IMPORTANT CONTEXT:
- You are emailing someone who WORKS at this company
- You are NOT an investor or analyst
- You are NOT pitching their company
- You are reaching out because their recent activity makes them a relevant prospect

Your goal:
- Show that you understand what the company is doing
- Connect that insight to a potential operational or growth challenge
- Gently position a conversation (not a sale)

Return output in EXACTLY this format:

SUBJECT:
<short, curiosity-driven subject line, 4–6 words>

BODY:
<single-paragraph cold email>

STRICT RULES FOR SUBJECT:
- 4 to 6 words
- No numbers
- No hype words
- No punctuation except hyphens

STRICT RULES FOR BODY:
- No subject line inside body
- No bullet points
- No markdown
- No greetings
- No investor language (ROI, returns, valuation, EPS, shareholders)
- 6 to 8 complete sentences
- 70 to 120 words
- Plain English prose
- Must sound like a human SDR

Company context:
{research}

Client rules:
{rag_context}
"""

    response = call_llm(prompt)

    # Parse response
    subject = ""
    body = ""

    if "SUBJECT:" in response and "BODY:" in response:
        subject = response.split("SUBJECT:")[1].split("BODY:")[0].strip()
        body = response.split("BODY:")[1].strip()
    else:
        body = response.strip()
        subject = f"Quick question about {company}"

    state["email_subject"] = subject
    state["email_draft"] = body

    return state
