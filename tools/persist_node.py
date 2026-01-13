from tools.gmail_tool import create_gmail_draft
from tools.sheets_tool import persist_to_sheets

def extract_subject_from_body(body_text: str, company: str = "") -> str:
    """Generate a concise subject line from email body"""
    import re
    
    # If it already has Subject: prefix, extract it
    if body_text.startswith("Subject:"):
        return body_text.split("\n", 1)[0].replace("Subject:", "").strip()
    
    # Find the first sentence (ends with . ! or ?)
    match = re.search(r'([^.!?]*[.!?])', body_text)
    
    if match:
        first_sentence = match.group(1).strip()
        
        # Extract key phrase: take first 8-10 words max
        words = first_sentence.replace('.', '').replace('!', '').replace('?', '').split()
        subject = ' '.join(words[:8])  # First 8 words
        
        # If company name in body, make it more targeted
        if company and len(subject) < 40:
            subject = f"Partnership Opportunity - {company}"
        
        # Ensure reasonable length (20-60 chars)
        if len(subject) > 60:
            subject = subject[:57] + "..."
        elif len(subject) < 10:
            subject = "Partnership Opportunity"
        
        return subject
    
    # Fallback
    return f"Partnership Opportunity - {company}" if company else "Partnership Opportunity"

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

    print(f"[DEBUG] email_draft exists: {bool(email_text)}")
    print(f"[DEBUG] lead_email: {lead_email}")

    if lead_email and email_text:
        try:
            # Handle both "Subject: ..." format and plain text
            if email_text.startswith("Subject:"):
                subject, body = email_text.split("\n", 1)
                subject = subject.replace("Subject:", "").strip()
                body = body.strip()
            else:
                # Extract subject from body and use rest as body
                subject = extract_subject_from_body(email_text, state.get("company", ""))
                body = email_text.strip()

            print(f"[DEBUG] Subject: {subject}")
            print(f"[DEBUG] Creating Gmail draft...")
            
            draft_id = create_gmail_draft(
                to_email=lead_email,
                subject=subject,
                body=body,
            )

            state["gmail_draft_id"] = draft_id
            print(f"[SUCCESS] Gmail draft created: {draft_id}")
        except Exception as e:
            print(f"[ERROR] Failed to create Gmail draft: {str(e)}")
            state["gmail_draft_error"] = str(e)
    else:
        print(f"[DEBUG] Skipping Gmail draft: lead_email={bool(lead_email)}, email_text={bool(email_text)}")

    return state
