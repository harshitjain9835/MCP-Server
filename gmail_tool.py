import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from auth import get_credentials

def create_email_draft(to: str, subject: str, body: str) -> dict:
    """Creates a draft email in the authenticated user's Gmail account."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Construct the MIME message
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject

    # Gmail API requires a base64url encoded string
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    draft_body = {
        'message': {
            'raw': encoded_message
        }
    }

    draft = service.users().drafts().create(userId='me', body=draft_body).execute()
    return draft