import fitz  # PyMuPDF
import re

# Extract text while keeping PDF structure and spacing
def extract_text_from_pdf(pdf_path):
    formatted_text = ""

    with fitz.open(pdf_path) as pdf_doc:
        for page in pdf_doc:
            blocks = page.get_text("blocks")  # Extract text as blocks (preserves layout)
            blocks.sort(key=lambda x: (x[1], x[0]))  # Sort by Y (top-down) then X (left-right)

            for block in blocks:
                text = block[4].strip()  # Extract actual text
                if text:
                    formatted_text += text + "\n\n"  # Add line breaks between blocks

            formatted_text += "\n\n"  # Keep space between pages

    return formatted_text.strip()
