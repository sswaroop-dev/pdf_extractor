"""Extraction Router for PDF processing with Gemini AI."""

import logging
from fastapi import APIRouter, HTTPException

from ...services.speed_feed.pdf_processor import PDFService

logger = logging.getLogger(__name__)

# This creates a 'group' of URLs related to extraction
router = APIRouter(prefix="/extract", tags=["Extraction"])
pdf_service = PDFService()


@router.post("/process-folder")
async def trigger_folder_extraction():
    """
    This endpoint looks at the 'data/speed_feed/vendor/haas/input' folder 
    and processes every PDF inside it using Gemini AI.
    
    Returns:
        Dictionary with status, files processed count, and results.
    """
    try:
        results = await pdf_service.process_all_pdfs()
        
        successful = [r for r in results if r.get("status") == "success"]
        failed = [r for r in results if r.get("status") == "failed"]
        
        return {
            "status": "success",
            "files_processed": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "data": results
        }
    except Exception as e:
        logger.error(f"Extraction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_extraction_status():
    """Check how many PDF files are waiting to be processed.
    
    Returns:
        Dictionary with pending files count and folder path.
    """
    pdf_files = list(pdf_service.input_dir.glob("*.pdf"))
    return {
        "pending_files": len(pdf_files),
        "folder": str(pdf_service.input_dir),
        "files": [f.name for f in pdf_files]
    }