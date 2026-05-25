from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from app.utils.ocr import extract_with_boxes, pdf_to_image_bytes
from app.utils.parser import detect_document_type, parse_document
from app.utils.highlighter import highlight_fields
from app.utils.exporter import export_both
from typing import List
import os
import io
import zipfile

router = APIRouter()

ALLOWED_IMAGES = ["image/jpeg", "image/png", "image/jpg", "image/tiff", "image/bmp"]
ALLOWED_PDF = ["application/pdf", "application/x-pdf", "binary/octet-stream", "application/octet-stream"]


async def process_single_file(file: UploadFile) -> dict:
    image_bytes = await file.read()

    is_pdf = (
        file.content_type in ALLOWED_PDF or
        (file.filename and file.filename.lower().endswith('.pdf'))
    )

    if is_pdf:
        try:
            image_bytes = pdf_to_image_bytes(image_bytes)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"PDF conversion failed: {str(e)}")
    elif file.content_type not in ALLOWED_IMAGES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not supported. Use JPG, PNG, TIFF, BMP or PDF."
        )

    ocr_result = extract_with_boxes(image_bytes)
    full_text = ocr_result['full_text']
    boxes = ocr_result['boxes']

    if not full_text:
        raise HTTPException(
            status_code=422,
            detail="Could not extract any text. Please upload a clearer image or PDF."
        )

    doc_type = detect_document_type(full_text)
    parsed_data = parse_document(full_text, doc_type)
    highlighted_image = highlight_fields(image_bytes, boxes, parsed_data, doc_type)
    exports = export_both(parsed_data, doc_type)

    return {
        "filename": file.filename,
        "doc_type": doc_type,
        "full_text": full_text,
        "parsed_data": parsed_data,
        "highlighted_image": highlighted_image,
        "boxes": boxes,
        "exports": exports,
        "is_pdf": is_pdf
    }


@router.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    result = await process_single_file(file)
    return result


@router.post("/extract-bulk")
async def extract_bulk(files: List[UploadFile] = File(...)):
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed at once.")

    results = []
    errors = []

    for file in files:
        try:
            result = await process_single_file(file)
            results.append(result)
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })

    return {
        "total": len(files),
        "success": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }


@router.get("/download/{filename}")
async def download_file(filename: str):
    filepath = os.path.join("exports", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type='application/octet-stream'
    )


@router.post("/download-bulk-zip")
async def download_bulk_zip(body: dict):
    filenames = body.get("filenames", [])
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename in filenames:
            filepath = os.path.join("exports", filename)
            if os.path.exists(filepath):
                zip_file.write(filepath, filename)

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=docusense_exports.zip"}
    )


@router.get("/health")
async def health():
    return {"status": "ok", "message": "DocuSense API is running"}