from fastapi import FastAPI, Request
from pdfParser import extract_invoice_data  # Import only parsing (calculations are separate)
import requests
import os
from dotenv import load_dotenv

# ✅ Load .env file from the .env directory inside GHL
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env/.env")
load_dotenv(dotenv_path=dotenv_path)

# ✅ Get OAuth Credentials from .env
CLIENT_ID = os.getenv("GHL_CLIENT_ID")
CLIENT_SECRET = os.getenv("GHL_CLIENT_SECRET")
AUTH_URL = os.getenv("GHL_AUTH_URL")

# ✅ Permanent Webhook URL (Replace with your Render URL)
WEBHOOK_URL = "https://your-app-name.onrender.com/webhook/invoice"  # Replace with actual Render URL

app = FastAPI()

# ✅ Function to Get OAuth Access Token
def get_ghl_access_token():
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

# ✅ Update GoHighLevel Webhook (Using Permanent Render URL)
def update_ghl_webhook():
    access_token = get_ghl_access_token()
    
    if not access_token:
        print("❌ Cannot update webhook without an access token!")
        return

    WEBHOOK_ENDPOINT = "https://api.gohighlevel.com/v1/webhooks"

    payload = {
        "event": "invoice_paid",
        "url": WEBHOOK_URL  # Use Render URL instead of Ngrok
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

# ✅ FastAPI Endpoint: Process Invoice
@app.post("/process_invoice")
async def process_invoice(request: Request):
    data = await request.json()
    print("📥 Received invoice:", data)

    pdf_path = "C:\\Users\\ryanc\\OneDrive\\Desktop\\GHL\\work_order.pdf"
    extracted_text = extract_invoice_data(pdf_path)

    return {"status": "success", "extracted_data": extracted_text}

# ✅ Start FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
