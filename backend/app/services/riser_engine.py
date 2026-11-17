import math
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Penetration:
    sheet: str
    floor_start: int
    floor_end: int
    x: float
    y: float


class RiserStackEngine:
    def __init__(self, riser_tag: str = "R-01", floor_start: int = 3, floor_end: int = 11):
        self.riser_tag = riser_tag
        self.floor_start = floor_start
        self.floor_end = floor_end

    def detect_and_route_offsets(self, penetrations: List[Penetration], tolerance_pixels: float = 10.0) -> List[Dict[str, Any]]:
        detected_offsets: List[Dict[str, Any]] = []

        for i in range(len(penetrations) - 1):
            lower = penetrations[i]
            upper = penetrations[i + 1]
            dx = upper.x - lower.x
            dy = upper.y - lower.y
            dist_px = math.hypot(dx, dy)

            if dist_px > tolerance_pixels:
                offset_feet = (dist_px / 12.0) * 1.0
                developed_length = offset_feet * 1.4142
                detected_offsets.append(
                    {
                        "riser_tag": self.riser_tag,
                        "transition_floor": lower.floor_end,
                        "lower_sheet": lower.sheet,
                        "upper_sheet": upper.sheet,
                        "horizontal_displacement_feet": round(offset_feet, 2),
                        "developed_pipe_length_feet": round(developed_length, 2),
                        "fitting_type": "TWO_45_DEGREE_BENDS",
                        "code_note": "Per 2025 PCNYS Section 710: sanitary offsets over a setback require full stack sizing review.",
                    }
                )

        return detected_offsets

    def calculate_stack_load_profile(self, floor_fixtures: Dict[int, List[str]], fixture_dfu: Dict[str, float], fixture_wsfu: Dict[str, float]) -> Dict[str, Any]:
        floor_data: Dict[int, Dict[str, Any]] = {}
        for floor in range(self.floor_start, self.floor_end + 1):
            floor_data[floor] = {
                "floor": floor,
                "fixtures": floor_fixtures.get(floor, []),
                "floor_dfu": 0.0,
                "floor_wsfu": 0.0,
                "cumulative_dfu": 0.0,
            }

        for floor, fixture_ids in floor_fixtures.items():
            if floor not in floor_data:
                continue
            for fixture_id in fixture_ids:
                floor_data[floor]["floor_dfu"] += fixture_dfu.get(fixture_id, 0.0)
                floor_data[floor]["floor_wsfu"] += fixture_wsfu.get(fixture_id, 0.0)

        running_dfu = 0.0
        for floor in sorted(floor_data.keys(), reverse=True):
            running_dfu += floor_data[floor]["floor_dfu"]
            floor_data[floor]["cumulative_dfu"] = running_dfu

        return {
            "riser_id": self.riser_tag,
            "tag": self.riser_tag,
            "system_type": "SANITARY_DRAIN",
            "pipe_size_inches": 3.0,
            "total_stack_dfu": running_dfu,
            "floors": [floor_data[floor] for floor in sorted(floor_data.keys())],
        }
