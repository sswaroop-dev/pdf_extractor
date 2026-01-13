"""PDF Structure Extraction Service.

This module provides functionality to extract structured content (text blocks and tables)
from PDF documents, returning a JSON-serializable representation of the document structure.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


class PDFStructureExtractor:
    """Extract text blocks and tables from PDF documents.
    
    This service provides a standalone, scalable solution for extracting structured
    content from PDFs. It identifies text blocks and tables, preserving their order
    and basic positional information.
    """

    def __init__(self):
        """Initialize the PDF structure extractor."""
        pass

    async def extract_structure(self, pdf_path: str | Path) -> Dict[str, Any]:
        """Extract structure from a PDF document.
        
        Args:
            pdf_path: Path to the PDF file (str or Path object).
            
        Returns:
            Dictionary containing structured PDF content with the following format:
            {
                "pages": [
                    {
                        "page_number": int,
                        "elements": [
                            {
                                "type": "text" | "table",
                                "order": int,
                                "content": str | List[List[str]],
                                "metadata": {
                                    "bbox": [x0, y0, x1, y1]
                                }
                            }
                        ]
                    }
                ],
                "summary": {
                    "total_pages": int,
                    "total_text_blocks": int,
                    "total_tables": int
                }
            }
            
        Raises:
            FileNotFoundError: If the PDF file does not exist.
            ValueError: If the file cannot be opened as a PDF.
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.is_file():
            raise ValueError(f"Path is not a file: {pdf_path}")
        
        # Run CPU-bound PDF processing in a thread pool
        return await asyncio.to_thread(self._extract_structure_sync, pdf_path)

    def _extract_structure_sync(self, pdf_path: Path) -> Dict[str, Any]:
        """Synchronous PDF structure extraction (runs in thread pool).
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            Dictionary containing structured PDF content.
        """
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            logger.error(f"Failed to open PDF {pdf_path}: {e}")
            raise ValueError(f"Cannot open PDF file: {e}") from e
        
        pages_data = []
        total_text_blocks = 0
        total_tables = 0
        
        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text blocks and tables
                text_blocks = self._extract_text_blocks(page)
                tables = self._extract_tables(page)
                
                # Combine and order elements
                elements = []
                order = 0
                
                # Add text blocks
                for block in text_blocks:
                    elements.append({
                        "type": "text",
                        "order": order,
                        "content": block["content"],
                        "metadata": {
                            "bbox": block["bbox"]
                        }
                    })
                    order += 1
                    total_text_blocks += 1
                
                # Add tables
                for table in tables:
                    elements.append({
                        "type": "table",
                        "order": order,
                        "content": table["content"],
                        "metadata": {
                            "bbox": table["bbox"]
                        }
                    })
                    order += 1
                    total_tables += 1
                
                # Sort elements by vertical position (top to bottom)
                elements.sort(key=lambda e: e["metadata"]["bbox"][1])
                # Reassign order after sorting
                for idx, element in enumerate(elements):
                    element["order"] = idx
                
                pages_data.append({
                    "page_number": page_num + 1,  # 1-indexed
                    "elements": elements
                })
        
        finally:
            doc.close()
        
        return {
            "pages": pages_data,
            "summary": {
                "total_pages": len(pages_data),
                "total_text_blocks": total_text_blocks,
                "total_tables": total_tables
            }
        }

    def _extract_text_blocks(self, page: fitz.Page) -> List[Dict[str, Any]]:
        """Extract text blocks from a PDF page.
        
        Args:
            page: PyMuPDF Page object.
            
        Returns:
            List of dictionaries containing text block data with 'content' and 'bbox' keys.
        """
        text_blocks = []
        
        try:
            # Get text blocks with bounding boxes
            blocks = page.get_text("blocks")
            
            for block in blocks:
                # block format: (x0, y0, x1, y1, "text", block_no, block_type)
                if len(block) >= 5:
                    bbox = list(block[0:4])  # [x0, y0, x1, y1]
                    text_content = block[4].strip()
                    
                    # Skip empty blocks
                    if text_content:
                        text_blocks.append({
                            "content": text_content,
                            "bbox": bbox
                        })
        
        except Exception as e:
            logger.warning(f"Error extracting text blocks from page {page.number}: {e}")
        
        return text_blocks

    def _extract_tables(self, page: fitz.Page) -> List[Dict[str, Any]]:
        """Extract tables from a PDF page.
        
        Uses PyMuPDF's table detection if available, otherwise falls back to
        heuristic-based detection.
        
        Args:
            page: PyMuPDF Page object.
            
        Returns:
            List of dictionaries containing table data with 'content' (as 2D list)
            and 'bbox' keys.
        """
        tables = []
        
        try:
            # Try PyMuPDF's built-in table detection (available in recent versions)
            if hasattr(page, "find_tables"):
                detected_tables = page.find_tables()
                
                for table in detected_tables:
                    # Extract table cells
                    table_data = []
                    for row in table.extract():
                        table_data.append(row)
                    
                    if table_data:
                        tables.append({
                            "content": table_data,
                            "bbox": list(table.bbox)  # [x0, y0, x1, y1]
                        })
            
            # Fallback: Use heuristic-based table detection
            if not tables:
                tables = self._detect_tables_heuristic(page)
        
        except Exception as e:
            logger.warning(f"Error extracting tables from page {page.number}: {e}")
            # Fallback to heuristic if built-in method fails
            try:
                tables = self._detect_tables_heuristic(page)
            except Exception as fallback_error:
                logger.error(f"Heuristic table detection also failed: {fallback_error}")
        
        return tables

    def _detect_tables_heuristic(self, page: fitz.Page) -> List[Dict[str, Any]]:
        """Heuristic-based table detection using text block alignment.
        
        This method identifies potential tables by looking for text blocks that
        are aligned in a grid-like pattern (multiple columns).
        
        Args:
            page: PyMuPDF Page object.
            
        Returns:
            List of dictionaries containing detected table data.
        """
        tables = []
        
        try:
            # Get text blocks with detailed information
            text_dict = page.get_text("dict")
            
            # Group blocks by similar y-coordinates (same row)
            blocks_by_row = {}
            tolerance = 5  # pixels tolerance for same row
            
            for block in text_dict.get("blocks", []):
                if "lines" not in block:
                    continue
                
                for line in block.get("lines", []):
                    if not line.get("spans"):
                        continue
                    
                    # Calculate average y-coordinate for the line
                    y_coords = [span.get("bbox", [])[1] for span in line["spans"] if span.get("bbox")]
                    if not y_coords:
                        continue
                    
                    avg_y = sum(y_coords) / len(y_coords)
                    
                    # Find existing row within tolerance
                    row_key = None
                    for key in blocks_by_row.keys():
                        if abs(key - avg_y) <= tolerance:
                            row_key = key
                            break
                    
                    if row_key is None:
                        row_key = avg_y
                    
                    if row_key not in blocks_by_row:
                        blocks_by_row[row_key] = []
                    
                    # Extract text from spans
                    line_text = " ".join([span.get("text", "") for span in line["spans"]])
                    if line_text.strip():
                        blocks_by_row[row_key].append({
                            "text": line_text.strip(),
                            "bbox": line.get("bbox", [0, 0, 0, 0]),
                            "x": line.get("bbox", [0, 0, 0, 0])[0] if line.get("bbox") else 0
                        })
            
            # Identify potential tables (rows with multiple columns)
            potential_table_rows = []
            for y, blocks in blocks_by_row.items():
                if len(blocks) >= 2:  # At least 2 columns suggests a table
                    # Sort blocks by x-coordinate
                    blocks.sort(key=lambda b: b["x"])
                    potential_table_rows.append({
                        "y": y,
                        "cells": [b["text"] for b in blocks],
                        "bbox": self._merge_bboxes([b["bbox"] for b in blocks])
                    })
            
            # Group consecutive rows into tables
            if potential_table_rows:
                # Sort by y-coordinate
                potential_table_rows.sort(key=lambda r: r["y"])
                
                # Simple grouping: consecutive rows form a table
                current_table = []
                for row in potential_table_rows:
                    if not current_table:
                        current_table = [row]
                    else:
                        # Check if this row is close to the previous one
                        last_y = current_table[-1]["y"]
                        if abs(row["y"] - last_y) <= 50:  # Within reasonable distance
                            current_table.append(row)
                        else:
                            # Save current table and start new one
                            if len(current_table) >= 2:  # At least 2 rows
                                table_data = [r["cells"] for r in current_table]
                                table_bbox = self._merge_bboxes([r["bbox"] for r in current_table])
                                tables.append({
                                    "content": table_data,
                                    "bbox": table_bbox
                                })
                            current_table = [row]
                
                # Don't forget the last table
                if len(current_table) >= 2:
                    table_data = [r["cells"] for r in current_table]
                    table_bbox = self._merge_bboxes([r["bbox"] for r in current_table])
                    tables.append({
                        "content": table_data,
                        "bbox": table_bbox
                    })
        
        except Exception as e:
            logger.warning(f"Error in heuristic table detection: {e}")
        
        return tables

    def _merge_bboxes(self, bboxes: List[List[float]]) -> List[float]:
        """Merge multiple bounding boxes into a single encompassing bbox.
        
        Args:
            bboxes: List of bounding boxes, each as [x0, y0, x1, y1].
            
        Returns:
            Merged bounding box as [x0, y0, x1, y1].
        """
        if not bboxes:
            return [0, 0, 0, 0]
        
        x0 = min(bbox[0] for bbox in bboxes)
        y0 = min(bbox[1] for bbox in bboxes)
        x1 = max(bbox[2] for bbox in bboxes)
        y1 = max(bbox[3] for bbox in bboxes)
        
        return [x0, y0, x1, y1]
