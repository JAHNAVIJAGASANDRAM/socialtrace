import json

def feature_fusion(features):
    weights = json.load(open("backend/app/engines/forensics/weights.json"))
    score = sum(weights[k] * features[k] for k in features)
    return min(max(score * 100, 0), 100)
