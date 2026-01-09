from .models.efficientnet import run_efficientnet_frames
from .metadata import metadata_integrity_check
from .utils import temporal_consistency

def video_forensics_pipeline(video_path, metadata):
    frame_scores = run_efficientnet_frames(video_path)

    return {
        "visual": sum(frame_scores) / len(frame_scores),
        "temporal": temporal_consistency(frame_scores),
        "metadata": metadata_integrity_check(metadata)
    }
