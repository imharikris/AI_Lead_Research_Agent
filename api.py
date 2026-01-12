from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.graph import build_agent_graph

app = FastAPI(title="Auto-SDR-Agent", description="Autonomous Lead Research Agent and Email Agent",version="1.0.0")

graph = build_agent_graph()

class LeadPayLoad(BaseModel):
    company:str
    email: str | None = None

@app.post("/run-agent")
def run_agent(PayLoad:LeadPayLoad):
    if not PayLoad.company:
        raise HTTPException(status_code=400, detail="Company is required")
    
    result = graph.invoke({"company":PayLoad.company, "lead_email":PayLoad.email})

    return {"status":"ok","email_draft": result.get("email_draft"),
        "sources": result.get("sources"),
        "gmail_draft_id": result.get("gmail_draft_id")}


