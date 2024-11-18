from pdf2image import convert_from_path
from easyocr import Reader

pdf_file = './sample-pdf/FIR_example.pdf'
images = convert_from_path(pdf_file)

# Create an EasyOCR reader instance
reader = Reader(['en', 'mr'])  # 'en' for English and 'mr' for Marathi

for i, image in enumerate(images):
    results = reader.readtext(image)
    print(f"Results for Page {i + 1}:")

    for result in results:
        print(result[1])  # Prints the recognized text
