import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
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

    sheet.append_row([
        state.get("company", "Unknown"),
        state.get("email_draft", "No Draft Generated"),
        ", ".join(sources_list[:5]),
    ])
