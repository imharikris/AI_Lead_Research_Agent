from langgraph.graph import StateGraph, END
from agent.planner import planner_node
from agent.evaluator import evaluate_node
from tools.tavily_search import research_node
from tools.email_writer import email_node

def build_agent_graph() -> StateGraph:
    graph  = StateGraph(dict)
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", research_node)
    graph.add_node("evaluator", evaluate_node)
    graph.add_node("email_writer", email_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "evaluator")
    graph.add_conditional_edges("evaluator", lambda s: "researcher" if not s["research_ok"] else "email_writer", {"researcher": "researcher", "email_writer": "email_writer"},)
    graph.add_edge("email_writer", END)
    return graph.compile()