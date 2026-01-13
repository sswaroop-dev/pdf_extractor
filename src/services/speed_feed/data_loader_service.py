from pathlib import Path
from typing import Optional


class DataLoaderService:
    def __init__(self):
        pass
    
    async def load_singular_pdf(self, path: Optional[str] = None) -> Path:
        """Load singular PDF file from data/speed_feed/vendor/haas/input.
        
        Args:
            path: Optional relative path from data/speed_feed/vendor/haas/input.
                  If None, loads from the input directory (expects single PDF file).
        
        Returns:
            Path object pointing to the PDF file.
            
        Raises:
            FileNotFoundError: If no PDF files are found in the input directory.
        """
        if path is None:
            # Default to loading from input directory
            input_dir = Path(__file__).parent.parent.parent / "data" / "speed_feed" / "vendor" / "haas" / "input"
            # Find first PDF file in input directory
            pdf_files = list(input_dir.glob("*.pdf"))
            if not pdf_files:
                raise FileNotFoundError(f"No PDF files found in {input_dir}")
            pdf_path = pdf_files[0]
        else:
            # Handle both relative paths from input directory and absolute paths
            if Path(path).is_absolute():
                pdf_path = Path(path)
            else:
                # Assume path is relative to input directory
                input_dir = Path(__file__).parent.parent.parent / "data" / "speed_feed" / "vendor" / "haas" / "input"
                pdf_path = input_dir / path
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.is_file():
            raise ValueError(f"Path is not a file: {pdf_path}")
        
        return pdf_path
