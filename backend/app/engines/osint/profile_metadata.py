def extract_profile_metadata(username, platform, profile_data=None):
    """
    profile_data can be manually provided or fetched via allowed APIs
    """

    if not profile_data:
        return {
            "username": username,
            "platform": platform,
            "profile_age_days": None,
            "followers": None,
            "following": None,
            "has_profile_image": None,
            "bio_length": None
        }

    return {
        "username": username,
        "platform": platform,
        "profile_age_days": profile_data.get("account_age_days"),
        "followers": profile_data.get("followers"),
        "following": profile_data.get("following"),
        "has_profile_image": bool(profile_data.get("profile_image")),
        "bio_length": len(profile_data.get("bio", ""))
    }
