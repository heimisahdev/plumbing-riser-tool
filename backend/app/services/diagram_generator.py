from typing import Any, Dict
import xml.etree.ElementTree as ET


class SchematicDiagramGenerator:
    def __init__(self):
        pass

    def generate_riser_svg(self, riser_id: str, width: int = 900) -> str:
        floors = [
            {"floor": 11, "fixtures": 5, "floor_dfu": 10.0, "cumulative_dfu": 26.0},
            {"floor": 10, "fixtures": 4, "floor_dfu": 8.0, "cumulative_dfu": 18.0},
            {"floor": 9, "fixtures": 3, "floor_dfu": 6.0, "cumulative_dfu": 12.0},
            {"floor": 8, "fixtures": 2, "floor_dfu": 4.0, "cumulative_dfu": 8.0},
            {"floor": 7, "fixtures": 4, "floor_dfu": 8.0, "cumulative_dfu": 20.0},
        ]

        floor_height = 70
        total_height = 120 + (len(floors) * floor_height)
        riser_x = 430

        root = ET.Element(
            "svg",
            {
                "viewBox": f"0 0 {width} {total_height}",
                "width": str(width),
                "height": str(total_height),
                "xmlns": "http://www.w3.org/2000/svg",
                "style": "background-color: #ffffff; font-family: sans-serif;",
            },
        )

        ET.SubElement(
            root,
            "rect",
            {"x": "40", "y": "20", "width": str(width - 80), "height": "60", "fill": "#f8fafc", "stroke": "#cbd5e1", "rx": "8"},
        )
        title = ET.SubElement(root, "text", {"x": "60", "y": "55", "font-size": "18", "font-weight": "bold", "fill": "#0f172a"})
        title.text = f"RISER DIAGRAM: {riser_id}"

        for idx, fl_data in enumerate(floors):
            y = 100 + idx * floor_height
            ET.SubElement(root, "line", {"x1": "80", "y1": str(y), "x2": str(width - 80), "y2": str(y), "stroke": "#e2e8f0", "stroke-dasharray": "4,4"})
            label = ET.SubElement(root, "text", {"x": "90", "y": str(y - 12), "font-size": "12", "font-weight": "bold", "fill": "#475569"})
            label.text = f"FL {fl_data['floor']}"
            if idx < len(floors) - 1:
                ET.SubElement(root, "line", {"x1": str(riser_x), "y1": str(y), "x2": str(riser_x), "y2": str(y + floor_height), "stroke": "#2563eb", "stroke-width": "4"})
            ET.SubElement(root, "line", {"x1": str(riser_x - 160), "y1": str(y + 26), "x2": str(riser_x), "y2": str(y + 26), "stroke": "#3b82f6", "stroke-width": "2.5"})
            ET.SubElement(root, "circle", {"cx": str(riser_x), "cy": str(y + 26), "r": "5", "fill": "#1d4ed8"})
            fixture_txt = ET.SubElement(root, "text", {"x": str(riser_x - 160), "y": str(y + 18), "font-size": "11", "fill": "#1e293b"})
            fixture_txt.text = f"{fl_data['fixtures']} Fixtures (+{fl_data['floor_dfu']} DFU)"
            cum_txt = ET.SubElement(root, "text", {"x": str(riser_x + 20), "y": str(y + 32), "font-size": "10", "font-weight": "bold", "fill": "#1e40af"})
            cum_txt.text = f"Cum: {fl_data['cumulative_dfu']} DFU"

        return ET.tostring(root, encoding="unicode")
