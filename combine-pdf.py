import os
import re
from PyPDF2 import PdfMerger

def sort_key(filename):
    """Extract leading numbers and convert them to an integer."""
    numbers = re.findall(r'^\d+', filename)
    return int(numbers[0]) if numbers else 0

def combine_pdfs(folder_path, output_filename):
    pdf_merger = PdfMerger()

    # List all PDF files in the folder and sort them
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    pdf_files.sort(key=sort_key)

    # Add each PDF to the merger
    for filename in pdf_files:
        pdf_merger.append(os.path.join(folder_path, filename))

    # Write out the combined PDF
    with open(output_filename, 'wb') as out:
        pdf_merger.write(out)

    print(f"Combined PDF saved as '{output_filename}'")

# Usage
folder_path = '.'  # Replace with the path to your folder
output_filename = 'combined.pdf'  # Name of the output file
combine_pdfs(folder_path, output_filename)

