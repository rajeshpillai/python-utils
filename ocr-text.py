from pdf2image import convert_from_path
import pytesseract

# Replace with the path to your PDF file
pdf_file = './sample-pdf/FIR_example.pdf'

# Convert PDF to list of images
print("Converting pdf to images...")
images = convert_from_path(pdf_file)

# Iterate over the images and apply OCR
for i, image in enumerate(images):
    text = pytesseract.image_to_string(image, lang='eng+mar')  # 'eng+mar' for English and Marathi
    # Save the text to a file or process it further
    with open(f'./output/page_{i}.txt', 'w', encoding='utf-8') as f:
        f.write(text)
