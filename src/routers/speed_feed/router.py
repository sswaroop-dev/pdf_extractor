"""Speed Feed Router.

Router for speed feed scraping endpoints. Can be integrated with FastAPI or other web frameworks.
"""

from pathlib import Path
from typing import Dict, Optional

from ...services.speed_feed import SpeedFeedScraperService


class SpeedFeedRouter:
    """Router for speed feed scraping operations."""

    def __init__(self):
        """Initialize the router with scraper service."""
        self.scraper_service = SpeedFeedScraperService()

    async def scrape_from_structure(
        self, structure_path: Optional[str] = None
    ) -> Dict:
        """Scrape data from extracted PDF structure file.
        
        Args:
            structure_path: Optional path to structure JSON file.
                          If None, uses the most recent structure file.
        
        Returns:
            Dictionary containing extracted speed and feed data.
        """
        path_obj = Path(structure_path) if structure_path else None
        return await self.scraper_service.scrape_from_structure(path_obj)

    async def scrape_from_pdf(self, pdf_path: Optional[str] = None) -> Dict:
        """Scrape data directly from PDF file.
        
        Args:
            pdf_path: Optional path to PDF file.
                    If None, loads from input directory.
        
        Returns:
            Dictionary containing extracted speed and feed data.
        """
        return await self.scraper_service.scrape_from_pdf(pdf_path)

    async def get_extracted_data(
        self, source: str = "structure", path: Optional[str] = None
    ) -> Dict:
        """Get extracted data from either structure file or PDF.
        
        Args:
            source: Source type - "structure" or "pdf". Defaults to "structure".
            path: Optional path to file. If None, uses defaults.
        
        Returns:
            Dictionary containing extracted speed and feed data.
        
        Raises:
            ValueError: If source is not "structure" or "pdf".
        """
        if source == "structure":
            return await self.scrape_from_structure(path)
        elif source == "pdf":
            return await self.scrape_from_pdf(path)
        else:
            raise ValueError(f"Invalid source: {source}. Must be 'structure' or 'pdf'")
