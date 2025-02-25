from fastapi import FastAPI, Request
import json

app = FastAPI()

# ✅ Add homepage to prevent 404
@app.get("/")
def home():
    return {"message": "Welcome to the Invoice Processing API"}

# ✅ GET Request Handler for Debugging
@app.get("/webhook/invoice")
def webhook_debug():
    return {"message": "Webhook is active, but use POST to send data"}

# ✅ Webhook Route to Receive Invoices from GHL (POST)
@app.post("/webhook/invoice")
async def receive_invoice_webhook(request: Request):
    try:
        invoice_data = await request.json()
        print("📥 FULL WEBHOOK DATA:", json.dumps(invoice_data, indent=4))

        # ✅ Extract fields from GHL webhook
        invoice_url = invoice_data.get("invoice", {}).get("url")
        contact_name = invoice_data.get("contact", {}).get("name")
        permit = invoice_data.get("custom_values", {}).get("permit")
        hoa = invoice_data.get("custom_values", {}).get("hoa")

        # ✅ Print extracted values for debugging
        print(f"🔹 Invoice URL: {invoice_url}")
        print(f"🔹 Contact Name: {contact_name}")
        print(f"🔹 Permit: {permit}")
        print(f"🔹 HOA: {hoa}")

        return {"status": "success", "message": "Invoice received", "invoice_url": invoice_url, "contact_name": contact_name, "permit": permit, "hoa": hoa}
    
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
