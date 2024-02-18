import os
import re
import argparse
from PyPDF2 import PdfMerger

def sort_key(filename):
    """Extract leading numbers (including decimals) and convert them to a tuple of integers."""
    numbers = re.findall(r'^(\d+(?:\.\d+)?)', filename)
    if numbers:
        parts = numbers[0].split('.')
        parts = [int(part) for part in parts]
        return tuple(parts)
    else:
        return (0,)

def combine_pdfs(folder_path, output_filename):
    pdf_merger = PdfMerger()

    # List all PDF files in the folder and sort them
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    pdf_files.sort(key=sort_key)

    # Add each PDF to the merger
    for filename in pdf_files:
        print("Merging file ", filename)
        pdf_merger.append(os.path.join(folder_path, filename))

    # Write out the combined PDF
    with open(output_filename, 'wb') as out:
        pdf_merger.write(out)

    print(f"Combined PDF saved as '{output_filename}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine PDF files from a specified folder into a single PDF, sorting them by leading numbers including decimals.")
    parser.add_argument("folder_path", type=str, help="The path to the folder containing PDF files to be combined.")
    parser.add_argument("output_filename", type=str, help="The name of the output combined PDF file.")
    
    args = parser.parse_args()
    
    combine_pdfs(args.folder_path, args.output_filename)


# EXAMPLE: python conbine-pdf.py /path/to/pdf/folder /home/user/merged_pdfs/output.pdf
# For sroted PDF: name the files in below numeric formaty any order supproted
# 1.some.pdf 
# 1.1 some.pdf 
# 1.1.someother.pdf
# 1.3_someother.pdf   


