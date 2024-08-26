import pdfplumber

def extract_pdf_lines(pdf_path):
    extracted_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            lines = page.extract_text().splitlines()
            for line_num, line in enumerate(lines):
                extracted_lines.append({
                    'page': page_num + 1,
                    'line_number': line_num + 1,
                    'text': line
                })
    return extracted_lines

# Example usage
pdf_path = "BOA.pdf"  # Path to your PDF file
extracted_data = extract_pdf_lines(pdf_path)
print(extracted_data)  # Print extracted data to see the format
