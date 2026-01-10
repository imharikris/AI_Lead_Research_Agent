def rag_node(state:dict) -> dict:
    rag_content = """
ICP:
- B2B SaaS companies
- 10-200 employees
- Founder or Head of Growth
Email Rules:
- 6 to 8 short lines
- 40 to 90 words total
- Friendly, professional tone
- One clear personalization hook
- One soft CTA
- No hype, no buzzwords
- Friendly and concise
- No buzzwords
- One clear Hook"""

    state["rag_content"] = rag_content
    return state
