import os
import pytesseract
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image

# Set the path to Tesseract OCR manually (if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

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
    """Convert image-based PDF pages to text using OCR."""
    images = convert_from_path(pdf_path)  # Convert PDF pages to images
    extracted_text = ""

    for img in images:
        extracted_text += pytesseract.image_to_string(img) + "\n"

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
