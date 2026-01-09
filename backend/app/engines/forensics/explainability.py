def generate_explainability(features, score):
    explanations = []
    for k, v in features.items():
        if v > 0.6:
            explanations.append(f"High anomaly detected in {k}")
    explanations.append(f"Final confidence score: {round(score,2)}")
    return explanations
