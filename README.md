# Google MCP Server

A FastAPI-based Model Context Protocol (MCP) style server for appending text to Google Docs and creating Gmail drafts. Features terminal-based execution approval to keep your data safe.

## 📂 Project Structure

- `server.py`: Core FastAPI server, API routing, and terminal approval logic.
- `auth.py`: Google OAuth2 authentication flow and credential management.
- `doc_tool.py`: Implementation for appending text to Google Docs.
- `gmail_tool.py`: Implementation for creating Gmail drafts.
- `deployment-plan.md`: Comprehensive reference guide for deployment.

## 🔌 API Endpoints

Detailed API documentation (Swagger UI) is automatically generated and available at the `/docs` endpoint when the server is running.

### 1. `GET /`
- **Description:** Check if the server is online.
- **Auth:** None required.

### 2. `POST /append_to_doc`
- **Description:** Appends text to the end of a specific Google Doc.
- **Auth:** `X-API-Key` header required.
- **Payload:**
  ```json
  {
    "doc_id": "your_document_id_here",
    "content": "Text to append"
  }
  ```

### 3. `POST /create_email_draft`
- **Description:** Creates a draft email in the authenticated user's Gmail account.
- **Auth:** `X-API-Key` header required.
- **Payload:**
  ```json
  {
    "to": "recipient@example.com",
    "subject": "Hello from MCP",
    "body": "Draft message content"
  }
  ```

## � Deployment (Railway)

Because Railway runs the application in a non-interactive environment, this guide utilizes the environment variable bypasses added to `server.py` and `auth.py`.

### Prerequisites
1. A GitHub repository containing the project files, including `requirements.txt` and `Procfile`.
2. A Railway account.
3. Your local `credential.json` and `token.json` files generated from the Google OAuth flow.

### Step-by-Step Deployment Guide

#### 1. Create a New Railway Project
- Log in to your Railway dashboard, click **"New Project"**, select **"Deploy from GitHub repo"**, and choose your repository.

#### 2. Configure Environment Variables
Railway needs your Google credentials and a flag to bypass the interactive terminal approval. Add the following in the **Variables** tab:
- `SKIP_TERMINAL_APPROVAL`: Set to `true`
- `GOOGLE_CREDENTIAL_JSON`: Copy and paste the entire contents of your local `credential.json` file.
- `GOOGLE_TOKEN_JSON`: Copy and paste the entire contents of your local `token.json` file.
- `MCP_API_KEY`: A secure random string to protect your API endpoints (e.g., `my-super-secret-key-123`).

#### 3. Deploy and Monitor
- Once variables are added, Railway will automatically trigger a deployment. Monitor build logs in the **Deployments** tab to ensure a successful build.

#### 4. Setup a Public Domain
- In the **Settings** tab under **Networking**, click **"Generate Domain"** to get the public URL for your FastAPI app.

### Important Considerations for Production
- **Security:** With `SKIP_TERMINAL_APPROVAL=true`, terminal interaction is bypassed. You must include an `X-API-Key` HTTP header matching your `MCP_API_KEY` environment variable when calling the API.
- **Token Expiration:** Railway uses an ephemeral filesystem. If your `token.json` expires and gets refreshed, the new token file will be lost upon the next restart. You'll need to periodically update the `GOOGLE_TOKEN_JSON` variable or migrate to a database for token storage.
