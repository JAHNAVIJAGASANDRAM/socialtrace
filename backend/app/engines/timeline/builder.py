from datetime import datetime

def build_timeline(evidence_store: dict):
    """
    evidence_store = EVIDENCE dict
    Returns sorted timeline events
    """

    events = []

    for case_id, evidences in evidence_store.items():
        for ev in evidences:
            events.append({
                "case_id": case_id,
                "filename": ev["original_filename"],
                "hash": ev["sha256"],
                "timestamp": datetime.fromisoformat(ev["uploaded_at"])
            })

    # sort by time
    events.sort(key=lambda x: x["timestamp"])

    # convert datetime back to string for API
    for e in events:
        e["timestamp"] = e["timestamp"].isoformat()

    return events

