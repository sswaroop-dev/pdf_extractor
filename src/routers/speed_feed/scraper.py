import asyncio
import json

from pathlib import Path
from typing import Dict, Optional

from ...services import DataLoaderService, PDFStructureExtractor, TempLLM


class SpeedFeedScraper:
    def __init__(self):
        self.llm = TempLLM()
        self.data_loader = DataLoaderService()
        self.pdf_extractor = PDFStructureExtractor()

    async def scrape(self, path: Optional[str] = None, save_to_raw: bool = True) -> Dict:
        """Scrape PDF from input directory and extract its structure.
        
        Args:
            path: Optional relative path from data/speed_feed/vendor/haas/input.
                  If None, loads first PDF from input directory.
            save_to_raw: If True, saves the extracted structure as JSON in raw directory.
        
        Returns:
            Dictionary containing the extracted PDF structure.
        """
        pdf_path = await self.data_loader.load_singular_pdf(path)
        structure = await self.pdf_extractor.extract_structure(pdf_path)
        
        if save_to_raw:
            await self._save_to_raw(pdf_path, structure)
        
        return structure

    async def _save_to_raw(self, pdf_path: Path, structure: Dict) -> Path:
        """Save extracted structure as JSON in raw directory.
        
        Args:
            pdf_path: Path to the source PDF file.
            structure: Extracted PDF structure dictionary.
        
        Returns:
            Path to the saved JSON file.
        """
        # Get raw directory path
        raw_dir = Path(__file__).parent.parent.parent / "data" / "speed_feed" / "vendor" / "haas" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        # Create output filename based on PDF filename
        pdf_stem = pdf_path.stem
        output_path = raw_dir / f"{pdf_stem}_structure.json"
        
        # Save as JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)
        
        print(f"Saved extracted structure to: {output_path}")
        return output_path


if __name__ == "__main__":
    scraper = SpeedFeedScraper()

    data = asyncio.run(scraper.scrape())

    print(f"\nExtraction complete! Found {data['summary']['total_pages']} pages, "
          f"{data['summary']['total_text_blocks']} text blocks, "
          f"and {data['summary']['total_tables']} tables.")
    