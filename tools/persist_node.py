from tools.gmail_tool import create_gmail_draft
from tools.sheets_tool import persist_to_sheets

def persist_node(state: dict) -> dict:
    """
    Final persistence step:
    - Logs output to Google Sheets (system of record)
    - Creates Gmail draft (human-in-the-loop)
    """

    # --- Always write to Sheets ---
    persist_to_sheets(state)

    # --- Optionally create Gmail draft ---
    email_text = state.get("email_draft", "")
    lead_email = state.get("lead_email")

    if lead_email and email_text.startswith("Subject:"):
        subject, body = email_text.split("\n", 1)
        subject = subject.replace("Subject:", "").strip()

        draft_id = create_gmail_draft(
            to_email=lead_email,
            subject=subject,
            body=body.strip(),
        )

        state["gmail_draft_id"] = draft_id

    return state
