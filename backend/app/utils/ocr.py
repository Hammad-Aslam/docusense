import pytesseract
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_bytes
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_to_image_bytes(file_bytes: bytes) -> bytes:
    pages = convert_from_bytes(file_bytes, dpi=200, poppler_path=r'C:\poppler-26.02.0\Library\bin')
    first_page = pages[0]
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text(image_bytes: bytes) -> str:
    img = preprocess_image(image_bytes)
    text = pytesseract.image_to_string(img)
    return text.strip()

def extract_with_boxes(image_bytes: bytes) -> dict:
    nparr = np.frombuffer(image_bytes, np.uint8)
    original = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT
    )

    boxes = []
    for i in range(len(data['text'])):
        if data['text'][i].strip() != '' and int(data['conf'][i]) > 60:
            boxes.append({
                'text': data['text'][i],
                'x': data['left'][i],
                'y': data['top'][i],
                'width': data['width'][i],
                'height': data['height'][i],
                'confidence': int(data['conf'][i])
            })

    full_text = pytesseract.image_to_string(gray)

    return {
        'full_text': full_text.strip(),
        'boxes': boxes,
        'image_width': original.shape[1],
        'image_height': original.shape[0]
    }