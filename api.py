from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from agent.graph import build_agent_graph

app = FastAPI(title="Auto-SDR-Agent", description="Autonomous Lead Research Agent and Email Agent",version="1.0.0")

graph = build_agent_graph()

class LeadPayLoad(BaseModel):
    company:str
    email: str | None = None
    row_index: int

@app.post("/run-agent")
async def run_agent(PayLoad:LeadPayLoad, background_tasks:BackgroundTasks):
    if not PayLoad.company:
        raise HTTPException(status_code=400, detail="Company is required")
    
    # Run agent in background so AppScript doesn't wait
    # This allows persist_node to update status to COMPLETED after agent finishes
    background_tasks.add_task(graph.invoke, {
        "company": PayLoad.company, 
        "lead_email": PayLoad.email, 
        "row_index": PayLoad.row_index
    })
    
    # Return immediately to AppScript (it will set status to SENT_TO_AGENT)
    # Agent will run in background and persist_node will update status to COMPLETED
    return {"status":"ok","message":"Agent started in background"}


