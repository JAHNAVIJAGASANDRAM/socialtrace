from .username_reuse import check_username_reuse
from .profile_metadata import extract_profile_metadata
from .linguistic import analyze_linguistic_patterns

def run_osint(username, platform, profile_data=None, posts=None):
    return {
        "username_reuse": check_username_reuse(username),
        "profile_metadata": extract_profile_metadata(username, platform, profile_data),
        "linguistic_analysis": analyze_linguistic_patterns(posts or [])
    }
