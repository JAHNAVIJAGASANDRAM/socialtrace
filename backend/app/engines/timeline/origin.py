def infer_origin(timeline_events):
    """
    Returns earliest appearance candidates
    """

    if not timeline_events:
        return None

    earliest = timeline_events[0]

    return {
        "origin_case": earliest["case_id"],
        "origin_file": earliest["filename"],
        "first_seen_at": earliest["timestamp"]
    }
