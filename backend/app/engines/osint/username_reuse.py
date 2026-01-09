def check_username_reuse(username):
    platforms = ["github.com", "reddit.com", "medium.com","instagram.com","pinterest.com","x.com","linkedin.com"]
    found = []

    for p in platforms:
        found.append({
            "platform": p,
            "url": f"https://{p}/{username}"
        })

    return found
