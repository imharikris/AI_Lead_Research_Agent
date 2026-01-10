import os 
import gspread
from google.oauth2.service_account import Credentials

SCOPE =["https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"]

def persist_node(state:dict) -> dict:
    creds = Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        scopes=SCOPE
    )
    client = gspread.authorize(creds)
    sheet_name = os.getenv("AI_Lead_Research_Agent_Data", "AI_SDR_Output")
    sheet = client.open(sheet_name).sheet1
    # Extract only the keys (URLs) if sources is a dict
    sources = state.get("sources", [])
    if isinstance(sources, dict):
        sources_list = list(sources.keys())
    else:
        sources_list = sources
    # Put Company in Col A, Email in Col B, and Sources in Col C
    sheet.append_row([
        state.get("company", "Unknown"),
        state.get("email_draft", "No Draft Generated"),
        ", ".join(sources_list[:5]) # Limit to 5 sources to keep row height small
    ])
    return state