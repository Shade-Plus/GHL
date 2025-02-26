from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import fitz  # PyMuPDF
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = FastAPI()

# Serve the UI
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return Path("src/templates/index.html").read_text()

# PDF Upload and Parsing Route
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(file_path)

        return {"status": "success", "extracted_text": extracted_text}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Function to Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_doc:
        for page in pdf_doc:
            text += page.get_text("text") + "\n"
    return text.strip()
