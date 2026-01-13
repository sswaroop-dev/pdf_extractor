"""Standalone FastAPI app for PDF extraction using Gemini AI."""

import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .gemini_client import GeminiClient
from .pdf_processor import PDFService


class TestPromptRequest(BaseModel):
    """Request model for test prompt."""
    prompt: str = "Say hello in one sentence."

logger = logging.getLogger(__name__)

# Initialize the standalone FastAPI app
app = FastAPI(title="Speed Feed PDF Extraction Service")
pdf_service = PDFService()
gemini_client = GeminiClient()


@app.post("/extract")
async def extract_all_documents():
    """
    Triggers the extraction for all PDFs in the input folder.
    Saves results as individual JSON files in the output folder.
    """
    try:
        # 1. Run your existing process_all_pdfs logic
        results = await pdf_service.process_all_pdfs()
        
        # 2. Save each result to a physical file in data/speed_feed/output
        # This makes sure you don't lose data if the browser closes
        saved_files = []
        for entry in results:
            if entry.get("status") == "success" and entry.get("data"):
                filename = entry["file"]
                raw_data = entry["data"]
                
                # Clean the filename for the output (e.g., report.pdf -> report.json)
                output_filename = f"{Path(filename).stem}.json"
                output_path = pdf_service.output_dir / output_filename
                
                # Save the AI response
                with open(output_path, "w", encoding="utf-8") as f:
                    # If Gemini returned a string, we save it directly
                    # If you want to force valid JSON, we'd use json.loads first
                    f.write(raw_data)
                
                saved_files.append(output_filename)
        
        successful = len([r for r in results if r.get("status") == "success"])
        failed = len([r for r in results if r.get("status") == "failed"])
        
        return {
            "message": f"Successfully processed {successful} files, {failed} failed.",
            "saved_files": saved_files,
            "saved_to": str(pdf_service.output_dir),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@app.get("/status")
async def get_status():
    """Check how many files are waiting to be processed."""
    pdf_files = list(pdf_service.input_dir.glob("*.pdf"))
    return {
        "pending_files": len(pdf_files),
        "folder": str(pdf_service.input_dir),
        "files": [f.name for f in pdf_files]
    }


@app.post("/test-gemini")
async def test_gemini(request: TestPromptRequest = TestPromptRequest()):
    """Test Gemini connection with a simple text prompt.
    
    This endpoint allows you to verify that Gemini API is working
    without needing to upload a PDF file.
    """
    try:
        response = await gemini_client.test_connection(request.prompt)
        return {
            "status": "success",
            "prompt": request.prompt,
            "response": response,
            "message": "Gemini API is working correctly!"
        }
    except Exception as e:
        logger.error(f"Gemini test failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Gemini test failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Unique port for this service