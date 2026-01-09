from tools.llm import call_llm

def email_node(state:dict) ->dict:
    company = state['company']
    research_summary = state.get('research_summary', '')

    prompt = f"""
    Write a short, personalized cold email;
    company: {company}
    Research Summary:
    {research_summary}
    Rules:
     - 5-6 lines
     - Professional and friendly tone
     - No sales hype
     - End with a soft cta
    Return only the email body.
    """
    email_body = call_llm(prompt)
    state['email_draft'] = email_body
    return state