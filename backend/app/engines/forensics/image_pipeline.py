from .models.xception import run_xception
from .metadata import metadata_integrity_check
from .utils import frequency_analysis, lighting_consistency

def image_forensics_pipeline(image_path, metadata):
    return {
        "cnn": run_xception(image_path),
        "frequency": frequency_analysis(image_path),
        "lighting": lighting_consistency(image_path),
        "metadata": metadata_integrity_check(metadata)
    }
