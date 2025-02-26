from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/webhook/invoice")
async def receive_invoice_webhook(request: Request):
    try:
        invoice_data = await request.json()
        print("Received Invoice Webhook:")

        extracted_data = {}

        # ✅ Dynamically extract and print all fields
        for key, value in invoice_data.items():
            print(f"{key}: {value}")
            extracted_data[key] = value  # Store all key-value pairs

        return {"status": "success", "message": "Webhook data received", "data": extracted_data}
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
