from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import uvicorn
import os

from docs_tool import append_to_doc
from gmail_tool import create_email_draft

app = FastAPI(
    title="Google MCP Server",
    description="MCP-style server for Google Docs and Gmail with terminal approval.",
    version="1.0.0"
)

# --- Security ---
API_KEY = os.environ.get("MCP_API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if API_KEY and api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API KEY")
    return api_key

# --- Pydantic Models for API Validation ---
class DocRequest(BaseModel):
    doc_id: str
    content: str

class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str

# --- Core Approval Logic ---
def require_approval(action_name: str, payload: dict) -> bool:
    """Prompts the terminal user to approve or deny an action."""
    # Bypass interactive prompt in non-interactive environments like Railway
    if os.environ.get("SKIP_TERMINAL_APPROVAL", "").lower() == "true":
        print(f"⚠️  Auto-approving {action_name} (SKIP_TERMINAL_APPROVAL is true)")
        return True

    print("\n" + "="*50)
    print(f"| ⚠️  ACTION REQUIRED: {action_name}")
    print(f"| 📦  Payload: {payload}")
    print("="*50)
    
    while True:
        response = input("Approve this action? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("✅ Action approved.")
            return True
        elif response in ['n', 'no']:
            print("❌ Action denied.")
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

# --- API Endpoints ---
@app.post("/append_to_doc", tags=["Google Docs"], dependencies=[Depends(get_api_key)])
def api_append_to_doc(request: DocRequest):
    """Appends content to a Google Doc after user approval."""
    # Ask for terminal approval before proceeding
    if not require_approval("append_to_doc", request.model_dump()):
        raise HTTPException(status_code=403, detail="Action denied by user in terminal.")
    
    try:
        result = append_to_doc(request.doc_id, request.content)
        print(f"Successfully appended content to doc_id: {request.doc_id}")
        return {"status": "success", "updates": result.get("replies")}
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_email_draft", tags=["Gmail"], dependencies=[Depends(get_api_key)])
def api_create_email_draft(request: EmailRequest):
    """Creates a Gmail draft after user approval."""
    # Ask for terminal approval before proceeding
    if not require_approval("create_email_draft", request.model_dump()):
        raise HTTPException(status_code=403, detail="Action denied by user in terminal.")
    
    try:
        result = create_email_draft(request.to, request.subject, request.body)
        print(f"Successfully created draft with id: {result.get('id')}")
        return {"status": "success", "draft_id": result.get("id")}
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Start the local development server
    # reload=True will automatically restart the server when you save a file
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Google MCP Server on port {port}")
    print(f"API documentation available at http://127.0.0.1:{port}/docs")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
