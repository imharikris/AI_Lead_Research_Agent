import os 
from tavily import TavilyClient

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def research_node(state:dict) ->dict:
    plan = state['plan']

    results = client.search(query=" ".join(plan.queries), max_results=5)

    summary = "\n".join(r["content"][:200] for r in results["results"])
    state["research_summary"] = summary[:800]
    state["sources"] = [r["url"] for r in results["results"]]
    return state