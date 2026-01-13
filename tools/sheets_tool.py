import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def persist_to_sheets(state: dict) -> None:
    creds = Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        scopes=SCOPE,
    )
    client = gspread.authorize(creds)

    sheet = client.open_by_key(
        os.getenv("OUTPUT_SHEET_ID")
    ).sheet1

    sources = state.get("sources", [])
    if isinstance(sources, dict):
        sources_list = list(sources.keys())
    else:
        sources_list = sources

    row_idx = state.get("row_index") 
    
    if row_idx:
        # Update specific columns:
        # Col 3: Status, Col 4: Email Draft, Col 5: Sources, Col 6: Processed At
        sheet.update_cell(row_idx, 3, "COMPLETED")
        sheet.update_cell(row_idx, 4, state.get("email_draft", ""))
        sheet.update_cell(row_idx, 5, ", ".join(sources_list[:3]))
        sheet.update_cell(row_idx, 6, datetime.now().isoformat())
        print(f"[SUCCESS] Updated row {row_idx}: Status=COMPLETED, Email Draft, Sources, Processed At")
    else:
        # Fallback if no row index
        sheet.append_row([state.get("company"), "No Index Found"])
        print(f"[WARNING] No row_index found, appended to sheet instead")
