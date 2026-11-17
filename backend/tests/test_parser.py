from app.parsers.pdf_parser import ArchitecturalPDFParser
from app.services.riser_engine import Penetration, RiserStackEngine


def test_extract_floor_range_grouped():
    parser = ArchitecturalPDFParser()
    start, end, floors, grouped = parser.extract_floor_range("OVERALL 3RD FLOOR-11TH FLOOR")
    assert (start, end, grouped) == (3, 11, True)
    assert floors == list(range(3, 12))


def test_riser_offset_detection():
    engine = RiserStackEngine("R-01", 3, 11)
    penetrations = [
        Penetration("A-103.00", 3, 8, 100, 100),
        Penetration("A-104.00", 9, 11, 170, 110),
    ]
    offsets = engine.detect_and_route_offsets(penetrations, tolerance_pixels=8)
    assert len(offsets) == 1
    assert offsets[0]["fitting_type"] == "TWO_45_DEGREE_BENDS"


def test_riser_profile_calculation():
    engine = RiserStackEngine("R-01", 3, 5)
    profile = engine.calculate_stack_load_profile(
        {3: ["WC", "LAV"], 4: ["WC"], 5: ["KS"]},
        {"WC": 4.0, "LAV": 1.0, "KS": 2.0},
        {"WC": 2.5, "LAV": 0.7, "KS": 1.4},
    )
    assert profile["total_stack_dfu"] >= 7.0
    assert profile["floors"][0]["floor"] == 3
