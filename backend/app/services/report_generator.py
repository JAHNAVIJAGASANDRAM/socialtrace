from datetime import datetime
from ..utils.serialization import to_python

def generate_case_report(
    case_id: str,
    evidences: dict,
    deepfake_result: dict | None = None,
    similarity_result: dict | None = None,
    timeline_result: dict | None = None,
    behavior_result: dict | None = None,
    graph_result: dict | None = None,
):
    """
    Generates a structured investigation-ready report
    """

    report = {
        "case_id": case_id,
        "generated_at": datetime.utcnow().isoformat(),
        "summary": {
            "total_evidence_items": len(evidences.get(case_id, [])),
            "deepfake_flagged": (
                deepfake_result["deepfake_score"] > 0.6
                if deepfake_result else False
            )
        },
        "evidence": evidences.get(case_id, []),
        "deepfake_analysis": deepfake_result,
        "similarity_analysis": similarity_result,
        "timeline_analysis": timeline_result,
        "behavior_analysis": behavior_result,
        "graph_analysis": graph_result,
        "disclaimer": (
            "This report is generated using automated analysis on publicly "
            "available and investigator-provided data. Identity attribution "
            "must be performed through lawful platform requests."
        )
    }

    return to_python(report)
