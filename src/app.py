from fastapi import FastAPI, Request
import json

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

# ✅ Start FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

