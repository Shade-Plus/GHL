from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/webhook/invoice")
async def receive_invoice_webhook(request: Request):
    try:
        # ✅ Extract all incoming webhook data
        invoice_data = await request.json()
        print("FULL WEBHOOK DATA:", json.dumps(invoice_data, indent=4))

        # ✅ Extract relevant fields from GHL webhook
        invoice_url = invoice_data.get("invoice", {}).get("url")
        contact_name = invoice_data.get("contact", {}).get("name")
        permit = invoice_data.get("custom_values", {}).get("permit")
        hoa = invoice_data.get("custom_values", {}).get("hoa")

        # ✅ Print extracted values for debugging
        print(f" Invoice URL: {invoice_url}")
        print(f" Contact Name: {contact_name}")
        print(f" Permit: {permit}")
        print(f" HOA: {hoa}")

        return {"status": "success", "message": "Invoice received", "invoice_url": invoice_url, "contact_name": contact_name, "permit": permit, "hoa": hoa}
    
    except Exception as e:
        print(f" Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
