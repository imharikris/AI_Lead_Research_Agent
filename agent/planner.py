from pydantic import BaseModel
from tools.llm import call_llm

class ResearchPlanner(BaseModel):
    company: str
    queries: list[str]

def planner_node(state:dict) ->dict:
    company = state['company']
    prompt = f""" 
    Create 3 concise Google search queries to research this company:{company}
    Return as a bullet list only."""
    text = call_llm(prompt)

    queries=[q.strip("- ").strip() for q in text.splitlines() if q.strip()]

    state["plan"] = ResearchPlanner(company=company, queries=queries)
    state["retry_count"] =0
    return state