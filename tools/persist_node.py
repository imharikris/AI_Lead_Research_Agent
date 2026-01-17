from tools.gmail_tool import create_gmail_draft
from tools.sheets_tool import persist_to_sheets


def persist_node(state: dict) -> dict:
    """
    Final persistence step:
    - Always logs output to Google Sheets (system of record)
    - Optionally creates Gmail draft (human-in-the-loop)
    """

    print("\n[PERSIST NODE] Starting persistence step")

    # --- Always persist to Google Sheets ---
    try:
        persist_to_sheets(state)
        print("[PERSIST NODE] Successfully saved to Google Sheets")
    except Exception as e:
        print(f"[ERROR] Failed to write to Google Sheets: {str(e)}")
        state["sheets_error"] = str(e)

    # --- Gmail Draft Creation ---
    email_body = state.get("email_draft", "")
    email_subject = state.get("email_subject", "")
    lead_email = state.get("lead_email")

    print(f"[DEBUG] lead_email present: {bool(lead_email)}")
    print(f"[DEBUG] email_subject: {email_subject}")
    print(f"[DEBUG] email_body length: {len(email_body.split())} words")

    if lead_email and email_body:
        try:
            print("[PERSIST NODE] Creating Gmail draft...")

            draft_id = create_gmail_draft(
                to_email=lead_email,
                subject=email_subject or "Quick question",
                body=email_body,
            )

            state["gmail_draft_id"] = draft_id
            print(f"[SUCCESS] Gmail draft created. Draft ID: {draft_id}")

        except Exception as e:
            print(f"[ERROR] Failed to create Gmail draft: {str(e)}")
            state["gmail_draft_error"] = str(e)

    else:
        print(
            "[PERSIST NODE] Skipping Gmail draft creation "
            f"(lead_email={bool(lead_email)}, email_body={bool(email_body)})"
        )

    print("[PERSIST NODE] Finished persistence step\n")
    return state
