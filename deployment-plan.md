# Deployment Plan for Railway

This document outlines the steps to deploy the Google MCP Server to Railway. Because Railway runs the application in a non-interactive environment, this guide utilizes the environment variable bypasses added to `server.py` and `auth.py`.

## Prerequisites
1. A GitHub repository containing the project files, including the `requirements.txt` and `Procfile`.
2. A Railway account.
3. Your local `credential.json` and `token.json` files generated from the Google OAuth flow.

## Step-by-Step Deployment Guide

### 1. Create a New Railway Project
- Log in to your Railway dashboard.
- Click **"New Project"**.
- Select **"Deploy from GitHub repo"**.
- Choose your `google-mcp-server` repository.

### 2. Configure Environment Variables
Railway needs your Google credentials and a flag to bypass the interactive terminal approval. Go to the **Variables** tab of your Railway service and add the following:

- `SKIP_TERMINAL_APPROVAL`: Set to `true`
- `GOOGLE_CREDENTIAL_JSON`: Copy and paste the entire contents of your local `credential.json` file here.
- `GOOGLE_TOKEN_JSON`: Copy and paste the entire contents of your local `token.json` file here.
- `MCP_API_KEY`: A secure random string to protect your API endpoints (e.g., `my-super-secret-key-123`).

*Note: Railway will inject these as environment variables, and `auth.py` will reconstruct the physical JSON files during startup.*

### 3. Deploy and Monitor
- Once the variables are added, Railway should automatically trigger a deployment. If not, trigger a manual deploy from the dashboard.
- Go to the **Deployments** tab to monitor the build logs.
- Ensure it successfully installs the requirements and runs the command from your `Procfile` (`uvicorn server:app --host 0.0.0.0 --port $PORT`).

### 4. Setup a Public Domain
- Go to the **Settings** tab of your Railway service.
- Scroll down to the **Networking** section.
- Click **"Generate Domain"** (or add a custom domain). This gives you the public URL for your FastAPI application.

## Important Considerations for Production
- **Security:** With `SKIP_TERMINAL_APPROVAL=true`, your endpoints bypass terminal interaction. An API Key authentication mechanism has been implemented. Any service calling your API must include an `X-API-Key` HTTP header that matches your `MCP_API_KEY` environment variable.
- **Token Expiration:** Railway uses an ephemeral filesystem. If your Google `token.json` expires and gets refreshed by `auth.py`, the new token file will be lost upon the next Railway restart or redeploy. You will eventually need to update the `GOOGLE_TOKEN_JSON` variable in Railway with a newly generated local token, or migrate the token storage to a database.