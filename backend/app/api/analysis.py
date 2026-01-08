from fastapi import APIRouter, HTTPException
from .cases import EVIDENCE
from ..engines.timeline.builder import build_timeline
from ..engines.timeline.origin import infer_origin
from ..engines.behaviour.cluster import cluster_accounts
from ..engines.behaviour.fingerprint import build_behavior_fingerprints
from ..engines.similarity.matcher import compare_phashes
from ..engines.graph.builder import build_investigation_graph
from ..engines.graph.analysis import analyze_graph
from ..services.report_generator import generate_case_report
from ..utils.serialization import to_python

import cv2
import os
import numpy as np

router = APIRouter()

# Simple heuristic-based deepfake trigger (placeholder)
def deepfake_trigger(video_path: str):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    blur_scores = []

    while frame_count < 30:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur_scores.append(blur)
        frame_count += 1

    cap.release()

    if not blur_scores:
        return 0.0, ["unable to read frames"]

    variance = np.var(blur_scores)

    # Heuristic: unstable sharpness → suspicious
    score = min(1.0, variance / 1000)

    reasons = []
    if score > 0.6:
        reasons.append("frame-level visual inconsistency")
    else:
        reasons.append("no strong manipulation indicators")

    return round(score, 2), reasons
import numpy as np

@router.post("/deepfake/{case_id}")
def run_deepfake(case_id: str):
    if case_id not in EVIDENCE:
        raise HTTPException(status_code=404, detail="No evidence found for case")

    video_path = EVIDENCE[case_id][0]["stored_path"]

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Evidence file missing")

    score, reasons = deepfake_trigger(video_path)

    return {
        "case_id": case_id,
        "deepfake_score": score,
        "indicators": reasons
    }
@router.post("/similarity/{case_id}")
def check_similarity(case_id: str):
    if case_id not in EVIDENCE:
        raise HTTPException(status_code=404, detail="No evidence found")

    current = EVIDENCE[case_id][0]
    matches = []

    for other_case, evidences in EVIDENCE.items():
        if other_case == case_id:
            continue

        for ev in evidences:
            if compare_phashes(current["phashes"], ev.get("phashes", [])):
                matches.append({
                    "matched_case": other_case,
                    "matched_file": ev["original_filename"]
                })

    return {
        "case_id": case_id,
        "similar_matches": matches
    }

@router.get("/timeline")
def get_timeline():
    timeline = build_timeline(EVIDENCE)
    origin = infer_origin(timeline)

    return {
        "total_events": len(timeline),
        "origin_candidate": origin,
        "timeline": timeline
    }

@router.get("/behavior")
def analyze_behavior():
    fingerprints = build_behavior_fingerprints(EVIDENCE)
    clusters = cluster_accounts(fingerprints)

    return {
        "total_accounts": len(fingerprints),
        "suspicious_clusters": clusters,
        "fingerprints": fingerprints
    }

@router.get("/graph")
def get_graph():
    graph = build_investigation_graph(EVIDENCE)
    central_nodes = analyze_graph(graph)

    nodes = [
        {"id": n, "type": graph.nodes[n]["type"]}
        for n in graph.nodes
    ]

    edges = [
        {
            "source": u,
            "target": v,
            "relation": d["relation"]
        }
        for u, v, d in graph.edges(data=True)
    ]

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "central_nodes": central_nodes,
        "nodes": nodes,
        "edges": edges
    }

@router.get("/report/{case_id}")
def generate_report(case_id: str):
    if case_id not in EVIDENCE:
        raise HTTPException(status_code=404, detail="Case not found")

    # Reuse existing analysis endpoints internally (simple approach)
    deepfake = None
    similarity = None

    # Deepfake (if evidence exists)
    try:
        from .analysis import run_deepfake
        deepfake = run_deepfake(case_id)
    except Exception:
        pass

    # Similarity
    try:
        from .analysis import check_similarity
        similarity = check_similarity(case_id)
    except Exception:
        pass

    # Timeline
    try:
        timeline = get_timeline()
    except Exception:
        timeline = None

    # Behavior
    try:
        behavior = analyze_behavior()
    except Exception:
        behavior = None

    # Graph
    try:
        graph = get_graph()
    except Exception:
        graph = None

    report = generate_case_report(
        case_id=case_id,
        evidences=EVIDENCE,
        deepfake_result=deepfake,
        similarity_result=similarity,
        timeline_result=timeline,
        behavior_result=behavior,
        graph_result=graph
    )

    return report



