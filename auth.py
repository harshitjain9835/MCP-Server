import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes required for both tools
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/gmail.compose'
]

def get_credentials():
    """Gets valid user credentials from storage or initiates the OAuth flow."""
    creds = None
    
    # In production, recreate the JSON files from environment variables if they don't exist
    if not os.path.exists('token.json') and os.environ.get('GOOGLE_TOKEN_JSON'):
        with open('token.json', 'w') as f:
            f.write(os.environ.get('GOOGLE_TOKEN_JSON'))
            
    if not os.path.exists('credential.json') and os.environ.get('GOOGLE_CREDENTIAL_JSON'):
        with open('credential.json', 'w') as f:
            f.write(os.environ.get('GOOGLE_CREDENTIAL_JSON'))
    
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("Initiating new OAuth2 flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credential.json', SCOPES
            )
            # Port 0 automatically finds an open port for the local callback
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            print("Credentials saved to token.json")
            
    return creds

if __name__ == "__main__":
    get_credentials()
