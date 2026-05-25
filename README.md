# DocuSense 🧾

> AI-powered document intelligence platform — extract structured data from bank slips, invoices, and ID cards using OCR + LLM.

![DocuSense](https://img.shields.io/badge/DocuSense-v1.0.0-00c896?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=nextdotjs)
![Llama](https://img.shields.io/badge/Llama_3.3_70B-Groq-f59e0b?style=flat-square)
![Tesseract](https://img.shields.io/badge/Tesseract_OCR-v5.5-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## What is DocuSense?

DocuSense is a full-stack document intelligence platform that combines **Tesseract OCR** and **Llama 3.3 70B** (via Groq) to automatically extract structured data from scanned documents. Upload a bank slip, invoice, or ID card — DocuSense reads it, identifies the document type, extracts key fields, highlights them visually on the original image, and exports the results to JSON or Excel.

Built as a portfolio project to demonstrate real-world AI integration, OCR pipelines, and production-grade API design.

---

## Features

- **OCR Extraction** — Tesseract v5.5 with OpenCV preprocessing (grayscale + Otsu thresholding)
- **AI Field Parsing** — Llama 3.3 70B via Groq structures raw OCR text into clean JSON
- **Auto Document Detection** — Automatically detects Bank Slips, Invoices, ID Cards, Receipts
- **Bounding Boxes** — Highlights every detected word on the document image with confidence scores
- **PDF Support** — Converts PDF pages to images via Poppler before OCR processing
- **Bulk Upload** — Process up to 10 documents at once with a results table view
- **Export** — Download results as JSON or Excel (.xlsx) per document or as a ZIP for bulk
- **History Panel** — Last 20 extractions saved in localStorage with one-click restore
- **REST API** — Full API with auto-generated Swagger UI at `/docs`
- **API Docs Page** — Developer documentation at `/api-docs` with Python, JS, and cURL examples

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| OCR Engine | Tesseract v5.5 | Text extraction from images |
| Image Processing | OpenCV + Pillow | Preprocessing and bounding boxes |
| AI / LLM | Llama 3.3 70B via Groq | Document type detection and field parsing |
| Backend | FastAPI + Python | REST API and file handling |
| Frontend | Next.js 15 + React | UI, bulk upload, history panel |
| PDF Conversion | pdf2image + Poppler | PDF to image conversion |
| Export | Pandas + OpenPyXL | JSON and Excel file generation |
| Environment | python-dotenv | Secure API key management |

---

## Architecture

```
User uploads Image or PDF
         ↓
[PDF?] → Poppler converts PDF page → PNG image
         ↓
OpenCV preprocesses image (grayscale + Otsu threshold)
         ↓
Tesseract OCR extracts:
  - Full text
  - Word-level bounding boxes + confidence scores
         ↓
Groq / Llama 3.3 70B:
  - Step 1: Detect document type (BANK_SLIP / INVOICE / ID_CARD / RECEIPT)
  - Step 2: Parse structured fields into clean JSON
         ↓
OpenCV draws colored bounding boxes on original image
         ↓
Pandas exports structured data to JSON + Excel
         ↓
Frontend displays:
  - Highlighted document image
  - Extracted fields panel
  - Raw OCR text
  - Export buttons
  - History panel
  - Bulk results table
```

---

## Project Structure

```
docusense/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── routers/
│   │   │   └── extract.py       # All API endpoints
│   │   └── utils/
│   │       ├── ocr.py           # Tesseract OCR + OpenCV
│   │       ├── parser.py        # Groq LLM field parsing
│   │       ├── highlighter.py   # Bounding box drawing
│   │       └── exporter.py      # JSON + Excel export
│   ├── uploads/                 # Temporary uploads (gitignored)
│   ├── exports/                 # Generated exports (gitignored)
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment variable template
└── frontend/
    ├── src/app/
    │   ├── page.tsx             # Main application page
    │   ├── globals.css          # Global styles
    │   ├── api-docs/
    │   │   └── page.tsx         # API documentation page
    │   └── components/
    │       ├── Uploader.tsx     # Single + bulk file upload
    │       ├── ResultPanel.tsx  # Extracted fields display
    │       ├── ImageViewer.tsx  # Highlighted document preview
    │       ├── HistoryPanel.tsx # Extraction history sidebar
    │       └── BulkResults.tsx  # Bulk results table
    └── package.json
```

---

## Prerequisites

Install these before running DocuSense:

### 1. Python 3.10+
Download from https://python.org

### 2. Node.js 18+
Download from https://nodejs.org

### 3. Tesseract OCR v5.5

**Windows:**
Download installer from https://github.com/UB-Mannheim/tesseract/wiki
- During installation check **Add to PATH**
- Default path: `C:\Program Files\Tesseract-OCR`

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Linux:**
```bash
sudo apt-get install tesseract-ocr
```

Verify:
```bash
tesseract --version
```

### 4. Poppler (for PDF support)

**Windows:**
Download from https://github.com/oschwartz10612/poppler-windows/releases/latest
- Extract to `C:\poppler-xx.xx.x`
- Add `C:\poppler-xx.xx.x\Library\bin` to your PATH environment variable

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Linux:**
```bash
sudo apt-get install poppler-utils
```

Verify:
```bash
pdftoppm -v
```

### 5. Groq API Key (Free)
1. Sign up at https://console.groq.com
2. Create an API key
3. Free tier includes 14,400 requests/day with Llama 3.3 70B

---

## Installation & Setup

### Step 1 — Clone the repository

```bash
git clone https://github.com/Hammad-Aslam/docusense.git
cd docusense
```

### Step 2 — Backend setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Create your .env file
# Windows:
copy .env.example .env
# macOS/Linux:
cp .env.example .env
```

Open `.env` and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

**Windows users only** — open `app/utils/ocr.py` and verify these two lines match your installation paths:

```python
# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Poppler path (inside pdf_to_image_bytes function)
pages = convert_from_bytes(file_bytes, dpi=200, poppler_path=r'C:\poppler-26.02.0\Library\bin')
```

**macOS/Linux users** — remove the `tesseract_cmd` line and `poppler_path` argument entirely as both are auto-detected.

### Step 3 — Start the backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend running at: http://localhost:8000
Swagger UI at: http://localhost:8000/docs

### Step 4 — Frontend setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend running at: http://localhost:3000
API Docs at: http://localhost:3000/api-docs

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/extract` | Extract single document (image or PDF) |
| POST | `/api/extract-bulk` | Extract up to 10 documents at once |
| GET | `/api/download/{filename}` | Download a JSON or Excel export file |
| POST | `/api/download-bulk-zip` | Download all exports as a single ZIP |

Full interactive API docs: http://localhost:3000/api-docs

---

## Supported Document Types

| Type | Extracted Fields |
|------|----------------|
| `BANK_SLIP` | transaction_id, date, time, sender_name, receiver_name, bank_name, amount, currency, transaction_type, reference_number, status |
| `INVOICE` | invoice_number, vendor_name, bill_to, date, due_date, subtotal, tax, total_amount, currency, line_items |
| `ID_CARD` | full_name, father_name, id_number, date_of_birth, issue_date, expiry_date, gender, address |
| `RECEIPT` | store_name, date, time, items, subtotal, tax, total, payment_method |

---

## Libraries Reference

### Backend

| Library | Version | Description |
|---------|---------|-------------|
| `fastapi` | 0.115.0 | Modern async Python web framework. Used to build all REST API endpoints with automatic OpenAPI/Swagger documentation |
| `uvicorn` | 0.30.6 | Lightning-fast ASGI server. Runs the FastAPI application in development and production |
| `pytesseract` | 0.3.13 | Python wrapper for Google's Tesseract OCR engine. Extracts text and word-level bounding boxes from images |
| `opencv-python` | 4.10.0 | Computer vision library. Used for image preprocessing (grayscale conversion, Otsu thresholding) and drawing colored bounding boxes on documents |
| `pillow` | 10.4.0 | Python Imaging Library. Handles image loading, format conversion, and manipulation before OCR |
| `pdf2image` | 1.17.0 | Converts PDF pages to PIL Image objects using Poppler. Enables PDF document support |
| `groq` | 0.11.0 | Official Groq Python SDK. Sends OCR text to Llama 3.3 70B for document type detection and structured field extraction |
| `pandas` | 2.2.3 | Data analysis library. Used to convert parsed JSON fields into structured DataFrames and export to Excel |
| `openpyxl` | 3.1.5 | Excel file writer. Used by Pandas to generate .xlsx export files with auto-adjusted column widths |
| `python-dotenv` | 1.0.1 | Loads environment variables from .env file. Keeps API keys out of source code |
| `python-multipart` | 0.0.9 | Parses multipart/form-data requests. Required by FastAPI to handle file uploads |

### Frontend

| Library | Version | Description |
|---------|---------|-------------|
| `Next.js` | 15 | React framework with App Router. Provides file-based routing, server components, and optimized builds |
| `React` | 18 | UI component library. All components (Uploader, ResultPanel, ImageViewer, HistoryPanel, BulkResults) are React functional components with hooks |
| `TypeScript` | 5 | Typed superset of JavaScript. Provides type safety across all components and interfaces |

---

## How It Works — Step by Step

1. **Upload** — User uploads an image (JPG, PNG, BMP, TIFF) or PDF via drag-and-drop or file browser
2. **PDF Conversion** — If PDF, Poppler converts the first page to a high-resolution PNG (200 DPI)
3. **Preprocessing** — OpenCV converts the image to grayscale and applies Otsu's thresholding to improve OCR accuracy on low-quality scans
4. **OCR** — Tesseract extracts the full text and generates word-level bounding boxes with confidence scores (words below 60% confidence are filtered out)
5. **Type Detection** — The OCR text is sent to Llama 3.3 70B via Groq with a classification prompt. The model returns one of: BANK_SLIP, INVOICE, ID_CARD, RECEIPT, UNKNOWN
6. **Field Parsing** — A second Groq call sends a document-type-specific prompt with a JSON template. Llama fills in the fields from the OCR text
7. **Highlighting** — OpenCV draws colored bounding boxes on the original image. Color varies by document type (green for bank slips, orange for invoices, red for ID cards)
8. **Export** — Pandas converts parsed fields to a DataFrame and saves JSON + Excel files to the exports directory
9. **Response** — FastAPI returns the doc type, parsed fields, base64-encoded highlighted image, bounding boxes, and export file paths
10. **Display** — The frontend renders the highlighted image, structured fields panel, raw OCR text, and download buttons

---

## Environment Variables

```env
# backend/.env
GROQ_API_KEY=your_groq_api_key_here
```

---
