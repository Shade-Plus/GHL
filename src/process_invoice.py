import os
from pdfParser import extract_invoice_data, extract_dimensions
from calculations import calculate_cut_sheet

# Set correct path to the PDF file
pdf_path = r"C:\Users\ryanc\OneDrive\Desktop\GHL\work_order.pdf"

if __name__ == "__main__":
    if os.path.exists(pdf_path):
        # Extract text and dimensions
        extracted_text = extract_invoice_data(pdf_path)
        extracted_text_combined = " ".join(extracted_text)
        dimensions = extract_dimensions(extracted_text_combined)

        # Perform calculations on extracted data
        cut_sheet_data = calculate_cut_sheet(dimensions)

        # Print extracted and calculated data
        print("\nExtracted Invoice Data:\n", extracted_text)
        print("\nCalculated Cut Sheet:\n", cut_sheet_data)
    else:
        print(f"Error: PDF file not found at {pdf_path}")
