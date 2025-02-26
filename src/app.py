from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/webhook/invoice")
async def receive_invoice_webhook(request: Request):
    try:
        invoice_data = await request.json()
        print("Received Invoice Webhook:", json.dumps(invoice_data, indent=4))

        # Extract fields from GHL webhook
        invoice_url = invoice_data.get("Invoice Url") or invoice_data.get("customData", {}).get("Invoice url")
        contact_name = invoice_data.get("customData", {}).get("contact name")
        amount = invoice_data.get("amount")  # This is missing from the payload

        # Debugging: Print extracted values
        print(f"Extracted Invoice URL: {invoice_url}")
        print(f"Extracted Contact Name: {contact_name}")
        print(f"Extracted Amount: {amount}")

        return {"status": "success", "message": "Invoice received", "invoice_url": invoice_url, "contact_name": contact_name, "amount": amount}
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
