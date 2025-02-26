from fastapi import FastAPI, Request
import json

app = FastAPI()

# Add homepage to prevent 404
@app.get("/")
def home():
    return {"message": "Welcome to the Invoice Processing API"}

# GET Request Handler for Debugging
@app.get("/webhook/invoice")
def webhook_debug():
    return {"message": "Webhook is active, but use POST to send data"}

# Webhook Route to Receive Invoices from GHL (POST)
@app.post("/webhook/invoice")
async def receive_invoice_webhook(request: Request):
    try:
        invoice_data = await request.json()
        print("Received Invoice Webhook:", json.dumps(invoice_data, indent=4))

        # Extract fields from GHL webhook
        invoice_url = invoice_data.get("invoice_url1") or invoice_data.get("invoice_url2")
        contact_name = invoice_data.get("contact", {}).get("name")
        amount = invoice_data.get("amount")

        # Print extracted values for debugging
        print(f"Invoice URL: {invoice_url}")
        print(f"Contact Name: {contact_name}")
        print(f"Amount: {amount}")

        return {"status": "success", "message": "Invoice received", "invoice_url": invoice_url, "contact_name": contact_name, "amount": amount}
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
