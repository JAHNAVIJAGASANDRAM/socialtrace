from datetime import datetime
from collections import defaultdict

def build_behavior_fingerprints(evidence_store: dict):
    """
    Builds behavior fingerprints per account
    """

    accounts = defaultdict(list)

    for evidences in evidence_store.values():
        for ev in evidences:
            if ev.get("username"):
                accounts[(ev["platform"], ev["username"])].append(ev)

    fingerprints = []

    for (platform, username), events in accounts.items():
        times = [datetime.fromisoformat(e["uploaded_at"]) for e in events]
        times.sort()

        gaps = []
        for i in range(1, len(times)):
            gaps.append((times[i] - times[i-1]).seconds)

        fingerprint = {
            "platform": platform,
            "username": username,
            "post_count": len(events),
            "first_seen": times[0].isoformat(),
            "last_seen": times[-1].isoformat(),
            "avg_gap_seconds": sum(gaps)/len(gaps) if gaps else None
        }

        fingerprints.append(fingerprint)

    return fingerprints
