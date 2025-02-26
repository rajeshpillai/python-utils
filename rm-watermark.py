import fitz  # PyMuPDF
import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import io

# Configure Tesseract path if needed (Windows users)
pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"

def remove_footer_text_and_watermark(pdf_path, output_path, search_texts, replace_text):
    """Removes text in the footer and replaces header text on ALL pages."""
    doc = fitz.open(pdf_path)
    text_found = False

    for page in doc:
        page_height = page.rect.height
        footer_area = fitz.Rect(0, page_height - 60, page.rect.width, page_height)  # Define footer area

        for search_text in search_texts:
            text_instances = page.search_for(search_text)  # Find text on each page

            if text_instances:
                text_found = True
                for inst in text_instances:
                    x0, y0, x1, y1 = inst

                    # ✅ Header: Replace text
                    if y0 < 100:
                        rect = fitz.Rect(x0, y0, x1, y1)
                        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))  # Erase text
                        page.insert_textbox(rect, replace_text, fontsize=10, color=(0, 0, 0))  # Insert new text
                    
                    # ✅ Footer: Completely erase text/watermark
                    elif y1 > page_height - 50:
                        rect = fitz.Rect(x0, y0, x1, y1)
                        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))  # Cover with white box

        # ✅ Ensure entire footer is blank, even if search text is not found
        page.draw_rect(footer_area, color=(1, 1, 1), fill=(1, 1, 1))  # Cover footer area with white

    if text_found:
        doc.save(output_path)
        print(f"✅ Header text replaced & footer removed on ALL pages: {pdf_path}")
    else:
        print(f"⚠️ No direct text found in {pdf_path}. Attempting OCR...")
        doc.close()
        perform_ocr_and_remove_footer(pdf_path, output_path, search_texts, replace_text)

def perform_ocr_and_remove_footer(pdf_path, output_path, search_texts, replace_text):
    """Performs OCR on ALL pages to detect & remove footer, and replace header text."""
    images = convert_from_path(pdf_path)
    new_doc = fitz.open()

    for i, image in enumerate(images):
        gray_image = image.convert("L")  # Convert to grayscale for better OCR
        extracted_text = pytesseract.image_to_string(gray_image)

        # ✅ Replace case-insensitive occurrences of the target word in headers
        for search_text in search_texts:
            extracted_text = extracted_text.replace(search_text, replace_text)

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        page = new_doc.new_page(width=image.width, height=image.height)
        pix = fitz.Pixmap(img_byte_arr)
        page.insert_image(page.rect, pixmap=pix)

        if replace_text in extracted_text:
            page.insert_text((50, 50), replace_text, fontsize=10, color=(0, 0, 0), overlay=True)

        # ✅ Completely erase footer area if OCR detects text there
        page_height = page.rect.height
        footer_area = fitz.Rect(0, page_height - 60, page.rect.width, page_height)
        page.draw_rect(footer_area, color=(1, 1, 1), fill=(1, 1, 1))  # Cover footer with white

    new_doc.save(output_path)
    new_doc.close()
    print(f"✅ OCR-based header text replaced & footer removed on ALL pages. Saved: {output_path}")

def process_pdfs_in_folder(folder_path):
    """Processes all PDFs in a folder, ensuring headers are replaced and footers removed on ALL pages."""
    output_folder = os.path.join(folder_path, "output")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)
            remove_footer_text_and_watermark(pdf_path, output_path, ["XYZ", "xyz"], "AI FOR ALL")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing PDFs: ").strip()
    process_pdfs_in_folder(folder_path)
    print("✅ Processing complete. Check the 'output' folder for results.")
