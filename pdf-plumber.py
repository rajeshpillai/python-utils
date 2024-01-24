import pdfplumber

output_file = 'extracted_text.txt'

# Replace 'yourfile.pdf' with the path to your PDF
with pdfplumber.open('sample-pdf/FIR_example.pdf') as pdf, open(output_file, 'w', encoding='utf-8') as file:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            file.write(text + '\n')
