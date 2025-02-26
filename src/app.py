import sys
import os

# Ensure the script can find `pdf_formatter.py`
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import shutil
import pdf_formatter  # Import PDF processing logic

app = FastAPI()

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")  # Use absolute path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload directory exists

# Serve the UI
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return Path("src/templates/index.html").read_text()

# PDF Upload and Processing Route
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Uploads a PDF file, extracts text, and returns structured invoice data.
    """
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract text using pdf_formatter
        extracted_text = pdf_formatter.extract_text_from_pdf(file_path)

        return {
            "status": "success",
            "filename": file.filename,
            "invoice_data": extracted_text
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Delete Uploaded PDF
@app.delete("/delete/{filename}")
async def delete_pdf(filename: str):
    """
    Deletes the specified PDF file from the uploads folder.
    """
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return JSONResponse(content={"status": "success", "message": f"Deleted {filename}"})
    else:
        return JSONResponse(content={"status": "error", "message": "File not found"}, status_code=404)

