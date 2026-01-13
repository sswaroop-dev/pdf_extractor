"""PDF Structure Extractor Script.

Simple script to load PDFs from input directory, extract structure,
and save results as JSON in raw directory.
"""

import asyncio
import json

from pathlib import Path
from typing import Optional

from ...services.speed_feed import DataLoaderService, PDFStructureExtractor


async def extract_and_save(path: Optional[str] = None) -> Path:
    """Load PDF, extract structure, and save to raw directory.
    
    Args:
        path: Optional relative path from data/speed_feed/vendor/haas/input.
              If None, loads first PDF from input directory.
    
    Returns:
        Path to the saved JSON file.
    """
    # Load PDF
    data_loader = DataLoaderService()
    pdf_path = await data_loader.load_singular_pdf(path)
    
    # Extract structure
    pdf_extractor = PDFStructureExtractor()
    structure = await pdf_extractor.extract_structure(pdf_path)
    
    # Save to raw directory
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
    result_path = asyncio.run(extract_and_save())
    
    # Load and display summary
    with open(result_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"\nExtraction complete! Found {data['summary']['total_pages']} pages, "
          f"{data['summary']['total_text_blocks']} text blocks, "
          f"and {data['summary']['total_tables']} tables.")
    