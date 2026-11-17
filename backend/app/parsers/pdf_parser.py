import os
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    import fitz  # type: ignore
except ImportError:  # pragma: no cover
    fitz = None


class ArchitecturalPDFParser:
    def __init__(self, target_dpi: int = 150):
        self.target_dpi = target_dpi
        self.zoom_factor = target_dpi / 72.0
        self.matrix = None if fitz is None else fitz.Matrix(self.zoom_factor, self.zoom_factor)

    def extract_floor_range(self, title_text: str) -> Tuple[int, int, List[int], bool]:
        text = title_text.upper().strip()

        range_match = re.search(
            r"(\d+)(?:ST|ND|RD|TH)?\s*(?:FLOOR|FL)?\s*[-–TO]+\s*(\d+)(?:ST|ND|RD|TH)?\s*(?:FLOOR|FL)?",
            text,
        )
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            if start > end:
                start, end = end, start
            return start, end, list(range(start, end + 1)), True

        single_match = re.search(
            r"(?:(\d+)(?:ST|ND|RD|TH)\s*(?:FLOOR|FL))|(?:(?:FLOOR|FL)\s*(\d+))",
            text,
        )
        if single_match:
            value = int(single_match.group(1) or single_match.group(2))
            return value, value, [value], False

        if "SUB-CELLAR" in text or "SUB CELLAR" in text:
            return -2, -2, [-2], False
        if "CELLAR" in text:
            return -1, -1, [-1], False
        if "BASEMENT" in text or "LOWER LEVEL" in text:
            return 0, 0, [0], False
        if "ROOF" in text or "BULKHEAD" in text:
            return 99, 99, [99], False

        return 1, 1, [1], False

    def extract_sheet_number(self, text: str) -> Optional[str]:
        match = re.search(r"\b([A-Z]{1,2}-\d{3}(?:\.\d{2})?)\b", text)
        return match.group(1) if match else None

    def process_pdf_page(self, pdf_path: str, page_number: int, output_dir: str) -> Dict[str, Any]:
        if fitz is None:
            raise ImportError("PyMuPDF is required to process architectural PDFs.")

        doc = fitz.open(pdf_path)
        if page_number >= len(doc):
            raise ValueError(f"Page {page_number} exceeds document page count.")

        page = doc[page_number]
        rect = page.rect
        width, height = rect.width, rect.height

        title_block_clip = fitz.Rect(width * 0.70, height * 0.65, width, height)
        title_block_text = page.get_text("text", clip=title_block_clip)

        if len(title_block_text.strip()) < 15:
            vertical_strip_clip = fitz.Rect(width * 0.85, 0, width, height)
            title_block_text = page.get_text("text", clip=vertical_strip_clip)

        if len(title_block_text.strip()) < 15:
            title_block_text = page.get_text("text")

        sheet_num = self.extract_sheet_number(title_block_text) or f"SHEET-{page_number + 1}"

        drawing_title = "UNTITLED FLOOR PLAN"
        for line in title_block_text.splitlines():
            line_clean = line.strip().upper()
            if any(k in line_clean for k in ["FLOOR", "OVERALL", "LEVEL", "PLAN", "ROOF", "CELLAR"]):
                if not re.search(r"\b[A-Z]-\d{3}\b", line_clean):
                    drawing_title = line.strip()
                    break

        floor_start, floor_end, covered_floors, is_grouped = self.extract_floor_range(drawing_title)

        os.makedirs(output_dir, exist_ok=True)
        pix = page.get_pixmap(matrix=self.matrix, alpha=False)
        rendered_filename = f"{sheet_num.replace('.', '_')}_page_{page_number + 1}.webp"
        rendered_path = os.path.join(output_dir, rendered_filename)
        pix.save(rendered_path)
        doc.close()

        return {
            "sheet_number": sheet_num,
            "drawing_title": drawing_title,
            "floor_start": floor_start,
            "floor_end": floor_end,
            "is_grouped_tier": is_grouped,
            "covered_floors": covered_floors,
            "pixel_width": pix.width,
            "pixel_height": pix.height,
            "rendered_image_url": f"/static/sheets/{rendered_filename}",
        }
