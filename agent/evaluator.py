MAX_RETRIES =2
MAX_LENGTH = 250

def evaluate_node(state:dict) ->dict:
    text = state.get("research_summary","")
    retries = state.get("retry_count",0)
    if len(text) >= MAX_LENGTH or retries >= MAX_RETRIES:
        state["research_ok"] = True
    else:
        state["research_ok"] = False
        state["retry_count"] = retries +1
    return state