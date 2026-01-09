from .image_pipeline import image_forensics_pipeline
from .video_pipeline import video_forensics_pipeline
from .fusion import feature_fusion
from .classifier import classify_media
from .explainability import generate_explainability
from .utils import detect_media_type
from .report import build_forensics_result

def analyze_media(media_path, metadata=None):
    media_type = detect_media_type(media_path)

    if media_type == "IMAGE":
        features = image_forensics_pipeline(media_path, metadata)
    elif media_type == "VIDEO":
        features = video_forensics_pipeline(media_path, metadata)
    else:
        raise ValueError("Unsupported media type")

    score = feature_fusion(features)
    classification = classify_media(score)
    explanation = generate_explainability(features, score)

    return build_forensics_result(
        media_type, score, classification, explanation
    )
