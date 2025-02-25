import pdfplumber
import os
import re

# Function to extract invoice text from a PDF
def extract_invoice_data(pdf_path):
    extracted_text = []
    
    if not os.path.exists(pdf_path):
        return {"error": "File not found"}
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

    return extracted_text

# Function to extract dimensions (parsing only)
def extract_dimensions(text):
    dimension_pattern = r"Size:\s*(\d+)'?(\d*)”?\s*[xX]\s*(\d+)'?(\d*)”?"
    matches = re.findall(dimension_pattern, text)
    dimensions = []

    for match in matches:
        width_feet, width_inches, length_feet, length_inches = match
        width = (int(width_feet) * 12) + (int(width_inches) if width_inches else 0)  # Convert to inches
        length = (int(length_feet) * 12) + (int(length_inches) if length_inches else 0)  # Convert to inches
        dimensions.append((width, length))  # Only extract raw dimensions, no calculations

    return dimensions
