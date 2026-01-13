"""PDF Processing Service using Gemini AI."""

import logging
from pathlib import Path
from typing import List, Dict, Any

from .gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class PDFService:
    """Service to process PDFs using Gemini AI for extraction."""

    def __init__(self):
        """Initialize PDF service with proper paths."""
        self.client = GeminiClient()
        
        # Use proper path resolution
        base_path = Path(__file__).parent.parent.parent.parent
        self.input_dir = base_path / "data" / "speed_feed" / "vendor" / "haas" / "input"
        self.output_dir = base_path / "data" / "speed_feed" / "vendor" / "haas" / "output"
        
        # Create folders if they don't exist
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def process_all_pdfs(self) -> List[Dict[str, Any]]:
        """Process all PDFs in the input directory using Gemini AI.
        
        Returns:
            List of dictionaries containing file name and extracted data.
        
        Raises:
            Exception: If processing fails for any file.
        """
        pdf_files = list(self.input_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.input_dir}")
            return []
        
        results = []

        for file_path in pdf_files:
            try:
                logger.info(f"Processing: {file_path.name}...")
                
                # The prompt we send to Gemini
                prompt = (
                    "Extract all the details from this pdf in a JSON format. "
                    "Note there are multiple texts and tables in the pdf and I want "
                    "the complete details of the tables in the right format. "
                    "Text can be stored separately for that page."
                )
                
                data = await self.client.extract_details(str(file_path), prompt)
                results.append({
                    "file": file_path.name,
                    "data": data,
                    "status": "success"
                })
                logger.info(f"Successfully processed: {file_path.name}")
                
            except Exception as e:
                logger.error(f"Failed to process {file_path.name}: {e}")
                results.append({
                    "file": file_path.name,
                    "data": None,
                    "status": "failed",
                    "error": str(e)
                })
        
        return results