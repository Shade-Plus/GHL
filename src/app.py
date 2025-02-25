from fastapi import FastAPI, Request
import json
import requests
import os
from dotenv import load_dotenv

# ✅ Load Environment Variables from `.env`
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env/.env")
load_dotenv(dotenv_path=dotenv_path)

# ✅ FastAPI App Initialization
app = FastAPI()

# ✅ Webhook Route to Receive Invoices from GHL
@app.post("/webhook/invoice")
async def receive_invoice_webhook(request: Request):
    try:
        invoice_data = await request.json()
        print("📥 Received Invoice Webhook:", json.dumps(invoice_data, indent=4))

        # TODO: Process invoice data here (parse PDF, extract details, etc.)

        return {"status": "success", "message": "Invoice received"}
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}

# ✅ Simple Homepage to Prevent 404
@app.get("/")
def home():
    return {"message": "Welcome to the Invoice Processing API"}

# ✅ Function to Get OAuth Access Token from GoHighLevel
def get_ghl_access_token():
    CLIENT_ID = os.getenv("GHL_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GHL_CLIENT_SECRET")
    AUTH_URL = os.getenv("GHL_AUTH_URL")

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(AUTH_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"❌ Failed to get GHL Access Token: {response.text}")
        return None

# ✅ Automatically Update Webhook in GoHighLevel
def update_ghl_webhook():
    access_token = get_ghl_access_token()
    
    if not access_token:
        print("❌ Cannot update webhook without an access token!")
        return

    WEBHOOK_ENDPOINT = "https://api.gohighlevel.com/v1/webhooks"

    payload = {
        "event": "invoice_paid",
        "url": "https://ghl-ldb2.onrender.com/webhook/invoice"  # Fixed URL for Render Deployment
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(WEBHOOK_ENDPOINT, json=payload, headers=headers)

    if response.status_code == 200:
        print("✅ GHL Webhook updated successfully!")
    else:
        print(f"❌ Failed to update GHL Webhook: {response.text}")

# ✅ Run webhook update when script starts
update_ghl_webhook()

# ✅ Start FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

