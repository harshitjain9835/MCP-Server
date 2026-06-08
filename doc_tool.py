from googleapiclient.discovery import build
from auth import get_credentials

def append_to_doc(doc_id: str, content: str) -> dict:
    """Appends text to the end of a specific Google Doc."""
    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)

    # Fetch the document to calculate where to insert the new text
    document = service.documents().get(documentId=doc_id).execute()
    body_content = document.get('body').get('content')
    
    # The last element in the body array gives us the end index.
    # We subtract 1 because the end index is exclusive.
    end_index = body_content[-1].get('endIndex') - 1

    # Prepend a newline to ensure the content starts on a new line.
    requests = [
        {
            'insertText': {
                'location': {
                    'index': end_index,
                },
                'text': "\n" + content
            }
        }
    ]

    result = service.documents().batchUpdate(
        documentId=doc_id, 
        body={'requests': requests}
    ).execute()
    
    return result
