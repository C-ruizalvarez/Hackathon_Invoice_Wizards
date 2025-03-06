import os
import pdfplumber
#import pytesseract
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from PIL import Image

# Set the path to Tesseract OCR manually (if needed)
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang="en")


def extract_text_from_image(image_path):
    """Extract text from an image using PaddleOCR."""
    ocr_result = ocr.ocr(image_path, cls=True)
    extracted_text = "\n".join([" ".join(line[1][0] for line in result) for result in ocr_result if result])
    return extracted_text

def extract_text_from_pdf(pdf_path):
    """Extract text from a text-based PDF using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def extract_text_from_image_pdf(pdf_path):
    """Convert image-based PDF pages to text using PaddleOCR."""
    images = convert_from_path(pdf_path)  # Convert PDF pages to images
    extracted_text = ""

    for img in images:
        img.save("temp.png")  # Save image temporarily
        extracted_text += extract_text_from_image("temp.png") + "\n"

    os.remove("temp.png")  # Remove temp image
    return extracted_text

def process_file(file_path):
    """Detect file type and extract text accordingly."""
    ext = os.path.splitext(file_path)[-1].lower()

    if ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        return extract_text_from_image(file_path)
    elif ext == ".pdf":
        text = extract_text_from_pdf(file_path)
        if not text.strip():  # If no text is extracted, try OCR
            print(f"No text found in {file_path}, using OCR...")
            text = extract_text_from_image_pdf(file_path)
        return text
    else:
        raise ValueError("Unsupported file format.")
