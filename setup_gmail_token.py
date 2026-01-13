#!/usr/bin/env python3
"""
Run this ONCE on your local machine to generate token.json
This will open a browser for you to authorize, then save the token.
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"

def setup_gmail_token():
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: {CREDENTIALS_FILE} not found!")
        return False
    
    print("=" * 60)
    print("GMAIL TOKEN SETUP")
    print("=" * 60)
    print("\nIMPORTANT:")
    print("1. A browser will open - DO NOT CLOSE IT")
    print("2. You MUST see 'Advance' link and click it")
    print("3. Then click 'Go to AI-SDR-Agent (unsafe)' to proceed")
    print("4. Grant ALL permissions requested")
    print("\nIf you see '403: access_denied':")
    print("   - Make sure you're logged in with the test user account")
    print("   - Check Google Cloud Console > OAuth Consent Screen > Test Users")
    print("\n" + "=" * 60)
    
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:8080"
    )
    
    # Add access_type for offline token refresh capability
    auth_url, state = flow.authorization_url(access_type='offline', prompt='consent')
    print(f"\nOpening browser to: {auth_url}\n")
    
    # Run local server
    creds = flow.run_local_server(port=8080, open_browser=True)
    
    # Save the token
    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! token.json created and saved.")
    print("=" * 60)
    print(f"\nFile location: {os.path.abspath(TOKEN_FILE)}")
    print("\nNext steps:")
    print("1. Commit token.json to your repository")
    print("2. Restart your FastAPI server")
    print("3. Test by adding a new row to Google Sheets with status 'NEW'")
    print("\nThe Gmail draft should now be created successfully!")
    
    return True

if __name__ == "__main__":
    setup_gmail_token()

