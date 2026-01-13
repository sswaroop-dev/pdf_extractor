# """Speed Feed Scraper Service.

# This service parses extracted PDF structure and extracts meaningful speed and feed data
# from tables and text blocks.
# """

# import json
# import re
# from pathlib import Path
# from typing import Any, Dict, List, Optional

# from .data_loader_service import DataLoaderService


# class SpeedFeedScraperService:
#     """Service to scrape speed and feed data from extracted PDF structure."""

#     def __init__(self):
#         """Initialize the scraper service."""
#         self.data_loader = DataLoaderService()

#     async def scrape_from_structure(
#         self, structure_path: Optional[Path] = None
#     ) -> Dict[str, Any]:
#         """Scrape data from extracted PDF structure JSON file.
        
#         Args:
#             structure_path: Path to the structure JSON file. If None, loads the most
#                           recent structure file from raw directory.
        
#         Returns:
#             Dictionary containing extracted speed and feed data.
#         """
#         if structure_path is None:
#             structure_path = await self._get_latest_structure_file()
        
#         # Load structure
#         with open(structure_path, "r", encoding="utf-8") as f:
#             structure = json.load(f)
        
#         # Extract data from structure
#         extracted_data = self._extract_data(structure)
        
#         return {
#             "source_file": str(structure_path),
#             "extraction_metadata": {
#                 "total_pages": structure.get("summary", {}).get("total_pages", 0),
#                 "total_text_blocks": structure.get("summary", {}).get("total_text_blocks", 0),
#                 "total_tables": structure.get("summary", {}).get("total_tables", 0),
#             },
#             "data": extracted_data,
#         }

#     async def scrape_from_pdf(
#         self, pdf_path: Optional[str] = None
#     ) -> Dict[str, Any]:
#         """Scrape data directly from PDF by first extracting structure.
        
#         Args:
#             pdf_path: Optional path to PDF file. If None, loads from input directory.
        
#         Returns:
#             Dictionary containing extracted speed and feed data.
#         """
#         from .pdf_extractor_service import PDFStructureExtractor
        
#         # Load PDF and extract structure
#         pdf_path_obj = await self.data_loader.load_singular_pdf(pdf_path)
#         pdf_extractor = PDFStructureExtractor()
#         structure = await pdf_extractor.extract_structure(pdf_path_obj)
        
#         # Extract data from structure
#         extracted_data = self._extract_data(structure)
        
#         return {
#             "source_file": str(pdf_path_obj),
#             "extraction_metadata": {
#                 "total_pages": structure.get("summary", {}).get("total_pages", 0),
#                 "total_text_blocks": structure.get("summary", {}).get("total_text_blocks", 0),
#                 "total_tables": structure.get("summary", {}).get("total_tables", 0),
#             },
#             "data": extracted_data,
#         }

#     def _extract_data(self, structure: Dict[str, Any]) -> Dict[str, Any]:
#         """Extract meaningful data from PDF structure.
        
#         Args:
#             structure: Extracted PDF structure dictionary.
        
#         Returns:
#             Dictionary containing extracted data organized by type.
#         """
#         extracted = {
#             "operation_types": [],
#             "tables": [],
#             "definitions": {},
#             "formulas": [],
#             "materials": [],
#             "speed_feed_data": [],
#         }
        
#         pages = structure.get("pages", [])
        
#         for page in pages:
#             page_num = page.get("page_number", 0)
#             elements = page.get("elements", [])
            
#             for element in elements:
#                 element_type = element.get("type")
#                 content = element.get("content", "")
                
#                 if element_type == "text":
#                     self._process_text_block(content, page_num, extracted)
#                 elif element_type == "table":
#                     self._process_table(element.get("content", []), page_num, extracted)
        
#         return extracted

#     def _process_text_block(
#         self, content: str, page_num: int, extracted: Dict[str, Any]
#     ) -> None:
#         """Process a text block to extract relevant information.
        
#         Args:
#             content: Text content of the block.
#             page_num: Page number where the text appears.
#             extracted: Dictionary to store extracted data.
#         """
#         content_lower = content.lower()
        
#         # Extract operation types (e.g., "Side Cutting", "Slotting")
#         operation_keywords = ["cutting", "slotting", "milling", "drilling", "turning"]
#         if any(keyword in content_lower for keyword in operation_keywords):
#             # Check if it's a title/header (short text, likely operation type)
#             if len(content.strip()) < 50 and content.strip():
#                 operation = content.strip()
#                 if operation not in extracted["operation_types"]:
#                     extracted["operation_types"].append({
#                         "name": operation,
#                         "page": page_num,
#                     })
        
#         # Extract formulas
#         formula_patterns = [
#             r"[vf]\s*=\s*[^=]+",  # Feed rate formulas
#             r"vc\s*=\s*[^=]+",  # Cutting speed formulas
#             r"n\s*=\s*[^=]+",  # Spindle speed formulas
#         ]
#         for pattern in formula_patterns:
#             matches = re.findall(pattern, content, re.IGNORECASE)
#             for match in matches:
#                 if match not in extracted["formulas"]:
#                     extracted["formulas"].append({
#                         "formula": match.strip(),
#                         "page": page_num,
#                     })
        
#         # Extract definitions (Symbol, Definition, Unit pattern)
#         if "symbol" in content_lower and "definition" in content_lower:
#             # This is likely a definition table header
#             pass  # Will be handled by table processing

#     def _process_table(
#         self, table_content: List[List[str]], page_num: int, extracted: Dict[str, Any]
#     ) -> None:
#         """Process a table to extract structured data.
        
#         Args:
#             table_content: Table content as 2D list of strings.
#             page_num: Page number where the table appears.
#             extracted: Dictionary to store extracted data.
#         """
#         if not table_content:
#             return
        
#         # Check if it's a definition table (has Symbol, Definition, Unit headers)
#         first_row = [cell.lower().strip() for cell in table_content[0]]
#         if "symbol" in str(first_row) and "definition" in str(first_row):
#             self._extract_definitions_table(table_content, page_num, extracted)
#             return
        
#         # Check if it's a data table (has numeric values, likely speed/feed data)
#         has_numeric_data = any(
#             re.search(r"\d+", str(cell)) for row in table_content for cell in row
#         )
        
#         if has_numeric_data and len(table_content) > 1:
#             # Try to extract speed/feed data
#             speed_feed_data = self._extract_speed_feed_table(
#                 table_content, page_num
#             )
#             if speed_feed_data:
#                 extracted["speed_feed_data"].extend(speed_feed_data)
        
#         # Store raw table for reference
#         extracted["tables"].append({
#             "page": page_num,
#             "rows": len(table_content),
#             "columns": len(table_content[0]) if table_content else 0,
#             "content": table_content,
#         })

#     def _extract_definitions_table(
#         self, table_content: List[List[str]], page_num: int, extracted: Dict[str, Any]
#     ) -> None:
#         """Extract definitions from a definition table.
        
#         Args:
#             table_content: Table content as 2D list.
#             page_num: Page number.
#             extracted: Dictionary to store extracted data.
#         """
#         if len(table_content) < 2:
#             return
        
#         # Skip header row, process data rows
#         for row in table_content[1:]:
#             if len(row) >= 3:
#                 symbol = row[0].strip()
#                 definition = row[1].strip()
#                 unit = row[2].strip() if len(row) > 2 else ""
                
#                 if symbol and definition:
#                     extracted["definitions"][symbol] = {
#                         "definition": definition,
#                         "unit": unit,
#                         "page": page_num,
#                     }

#     def _extract_speed_feed_table(
#         self, table_content: List[List[str]], page_num: int
#     ) -> List[Dict[str, Any]]:
#         """Extract speed and feed data from a table.
        
#         Args:
#             table_content: Table content as 2D list.
#             page_num: Page number.
        
#         Returns:
#             List of extracted speed/feed records.
#         """
#         extracted_records = []
        
#         if len(table_content) < 2:
#             return extracted_records
        
#         # Try to identify header row
#         header_row_idx = 0
#         headers = [cell.strip().lower() for cell in table_content[0]]
        
#         # Look for common speed/feed column names
#         speed_keywords = ["speed", "rpm", "n", "spindle"]
#         feed_keywords = ["feed", "vf", "ipm", "in/min"]
#         material_keywords = ["material", "iso", "type"]
#         tool_keywords = ["tool", "diameter", "d", "size"]
        
#         # Identify column indices
#         speed_col_idx = None
#         feed_col_idx = None
#         material_col_idx = None
#         tool_col_idx = None
        
#         for idx, header in enumerate(headers):
#             if any(kw in header for kw in speed_keywords):
#                 speed_col_idx = idx
#             if any(kw in header for kw in feed_keywords):
#                 feed_col_idx = idx
#             if any(kw in header for kw in material_keywords):
#                 material_col_idx = idx
#             if any(kw in header for kw in tool_keywords):
#                 tool_col_idx = idx
        
#         # Process data rows
#         for row_idx in range(1, len(table_content)):
#             row = table_content[row_idx]
#             if not row:
#                 continue
            
#             record = {
#                 "page": page_num,
#                 "row_index": row_idx,
#             }
            
#             # Extract values based on identified columns
#             if speed_col_idx is not None and speed_col_idx < len(row):
#                 speed_val = self._extract_numeric_value(row[speed_col_idx])
#                 if speed_val is not None:
#                     record["speed_rpm"] = speed_val
            
#             if feed_col_idx is not None and feed_col_idx < len(row):
#                 feed_val = self._extract_numeric_value(row[feed_col_idx])
#                 if feed_val is not None:
#                     record["feed_ipm"] = feed_val
            
#             if material_col_idx is not None and material_col_idx < len(row):
#                 material_val = row[material_col_idx].strip()
#                 if material_val:
#                     record["material"] = material_val
            
#             if tool_col_idx is not None and tool_col_idx < len(row):
#                 tool_val = row[tool_col_idx].strip()
#                 if tool_val:
#                     record["tool_info"] = tool_val
            
#             # If we extracted at least speed or feed, add the record
#             if "speed_rpm" in record or "feed_ipm" in record:
#                 extracted_records.append(record)
        
#         return extracted_records

#     def _extract_numeric_value(self, text: str) -> Optional[float]:
#         """Extract numeric value from text string.
        
#         Args:
#             text: Text string that may contain numbers.
        
#         Returns:
#             Extracted numeric value or None if not found.
#         """
#         if not text:
#             return None
        
#         # Remove common units and extract number
#         text_clean = re.sub(r"[^\d.,\-]", "", str(text))
#         text_clean = text_clean.replace(",", "")
        
#         try:
#             return float(text_clean)
#         except (ValueError, AttributeError):
#             return None

#     async def _get_latest_structure_file(self) -> Path:
#         """Get the most recent structure JSON file from raw directory.
        
#         Returns:
#             Path to the latest structure file.
        
#         Raises:
#             FileNotFoundError: If no structure files are found.
#         """
#         raw_dir = (
#             Path(__file__).parent.parent.parent
#             / "data"
#             / "speed_feed"
#             / "vendor"
#             / "haas"
#             / "raw"
#         )
        
#         structure_files = list(raw_dir.glob("*_structure.json"))
#         if not structure_files:
#             raise FileNotFoundError(f"No structure files found in {raw_dir}")
        
#         # Return the most recently modified file
#         return max(structure_files, key=lambda p: p.stat().st_mtime)
