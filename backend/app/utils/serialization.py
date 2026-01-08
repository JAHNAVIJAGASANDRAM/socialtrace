import numpy as np

def to_python(obj):
    """
    Recursively convert NumPy types to native Python types
    so FastAPI can serialize them.
    """
    if isinstance(obj, np.generic):
        return obj.item()
    elif isinstance(obj, dict):
        return {k: to_python(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_python(v) for v in obj]
    else:
        return obj
