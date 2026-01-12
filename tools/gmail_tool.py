import base64
import os 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES =["https://www.googleapis.com/auth/gmail.compose"]
TOKEN_FILE = "token.json"

def get_gmail_service():
    if os.path.exists(TOKEN_FILE):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(TOKEN_FILE,scopes=SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json",scopes=SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1",credentials=creds)

def create_gmail_draft(to_email: str, subject: str, body: str):
    service = get_gmail_service()
    message = f"To:{to_email}\nSubject:{subject}\n\n{body}"
    raw = base64.urlsafe_b64decode(message.encode()).decode()
    draft = service.users().drafts().create(
        userId ="me",
        body = {message:{"raw":raw}}
    ).execute()

    return draft["id"]
