import base64
import os 
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from email.message import EmailMessage

SCOPES =["https://www.googleapis.com/auth/gmail.compose"]
SERVICE_ACCOUNT_FILE = "service_account.json"

def get_gmail_service():
    """Use service account for server-side authentication (no browser popup)"""
    from google.oauth2.credentials import Credentials
    
    TOKEN_FILE = "token.json"
    
    # Prefer existing token.json (fastest, no auth needed)
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, scopes=SCOPES)
            print(f"[INFO] Using existing token from {TOKEN_FILE}")
            return build("gmail", "v1", credentials=creds)
        except Exception as e:
            print(f"[WARNING] Token file invalid: {e}, trying service account...")
    
    # Try service account (server-side, no user interaction needed)
    try:
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            creds = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, 
                scopes=SCOPES
            )
            print(f"[INFO] Using service account from {SERVICE_ACCOUNT_FILE}")
            return build("gmail", "v1", credentials=creds)
    except Exception as e:
        print(f"[ERROR] Service account failed: {str(e)}")
    
    # Fallback to OAuth (will prompt for browser login)
    print("[WARNING] No token.json or service account found, attempting OAuth...")
    from google_auth_oauthlib.flow import InstalledAppFlow
    
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())
    
    return build("gmail", "v1", credentials=creds)

def create_gmail_draft(to_email: str, subject: str, body: str):
    """Create a Gmail draft with error handling"""
    try:
        service = get_gmail_service()
        
        # Create a proper email object
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to_email
        message['Subject'] = subject
        
        # Encode correctly
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        create_message = {
            'message': {
                'raw': raw_message
            }
        }
        
        draft = service.users().drafts().create(userId="me", body=create_message).execute()
        draft_id = draft.get("id")
        print(f"[SUCCESS] Gmail draft created: {draft_id}")
        return draft_id
        
    except Exception as e:
        print(f"[ERROR] create_gmail_draft failed: {str(e)}")
        raise
