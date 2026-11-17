from typing import Any, Dict, List

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.services.diagram_generator import SchematicDiagramGenerator
from app.services.riser_engine import Penetration, RiserStackEngine

router = APIRouter()


@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@router.post("/selection/lasso")
def lasso_selection(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    polygon = payload.get("polygon", [])
    assigned_riser = payload.get("assigned_riser_tag", "R-01")
    selected = []
    for index, point in enumerate(polygon[:10]):
        selected.append({"id": f"pop-{index + 1}", "riser": assigned_riser, "x": point.get("x", 0), "y": point.get("y", 0)})
    return selected


@router.get("/deliverables/risers/{riser_id}/diagram.svg")
def get_riser_diagram(riser_id: str) -> PlainTextResponse:
    generator = SchematicDiagramGenerator()
    svg = generator.generate_riser_svg(riser_id)
    return PlainTextResponse(content=svg, media_type="image/svg+xml")


@router.get("/deliverables/projects/{project_id}/takeoff/export.csv")
def export_takeoff_csv(project_id: str) -> PlainTextResponse:
    csv = "fixture_id,fixture_name,quantity,unit,dfu\nWC,Water Closet,12,ea,48\nLAV,Lavatory,8,ea,8\nKS,Kitchen Sink,4,ea,8\n"
    return PlainTextResponse(content=csv, media_type="text/csv")


@router.get("/debug/riser-profile")
def debug_riser_profile() -> Dict[str, Any]:
    engine = RiserStackEngine(riser_tag="R-01", floor_start=3, floor_end=11)
    floor_fixtures = {
        3: ["WC", "LAV"],
        4: ["WC"],
        5: ["KS", "LAV"],
        6: ["WC"],
    }
    fixture_dfu = {"WC": 4.0, "LAV": 1.0, "KS": 2.0}
    fixture_wsfu = {"WC": 2.5, "LAV": 0.7, "KS": 1.4}

    profile = engine.calculate_stack_load_profile(floor_fixtures, fixture_dfu, fixture_wsfu)
    penetrations = [
        Penetration("A-103.00", 3, 9, 100, 100),
        Penetration("A-104.00", 10, 11, 130, 105),
    ]
    offsets = engine.detect_and_route_offsets(penetrations, tolerance_pixels=8)
    return {"profile": profile, "offsets": offsets}
