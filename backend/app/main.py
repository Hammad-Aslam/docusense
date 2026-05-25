from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.extract import router as extract_router
import os

app = FastAPI(
    title="DocuSense API",
    description="Intelligent document OCR and field extraction for invoices, bank slips and ID cards",
    version="1.0.0"
)

# CORS - allows frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create upload and export folders if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("exports", exist_ok=True)

# Register routers
app.include_router(extract_router, prefix="/api", tags=["Document Extraction"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to DocuSense API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }