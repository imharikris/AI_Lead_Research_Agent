from langgraph.graph import StateGraph, END
from agent.planner import planner_node
from agent.evaluator import evaluate_node
from tools.tavily_search import research_node
from tools.email_writer import email_node
from agent.validator import validator_node
from tools.sheets_tool import persist_node
from tools.rag_retriever import rag_node

def build_agent_graph() -> StateGraph:
    graph  = StateGraph(dict)
    # ---Nodes---
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", research_node)
    graph.add_node("evaluator", evaluate_node)
    graph.add_node("email_writer", email_node)
    graph.add_node("validator", validator_node)
    graph.add_node("persist", persist_node)
    graph.add_node("rag_retriever", rag_node)

    #---Entry point Edge----
    graph.set_entry_point("planner")

    #---Normal Flow Edges---
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "evaluator")

    #--Conditional Edges---
    graph.add_conditional_edges("evaluator", lambda s: "researcher" if not s["research_ok"] else "rag_retriever", {"researcher": "researcher", "rag_retriever": "rag_retriever"},)

    #---Final Pipeline Edges---
    graph.add_edge("rag_retriever", "email_writer")
    graph.add_edge("email_writer", "validator")
    graph.add_conditional_edges("validator", lambda s: "email_writer" if not s["email_valid"] else "persist", {"email_writer": "email_writer", "persist": "persist"},)
    graph.add_edge("persist", END)

    return graph.compile()