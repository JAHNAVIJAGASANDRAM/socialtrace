def cluster_accounts(fingerprints, time_threshold=300):
    """
    Simple clustering based on similar posting gaps
    """

    clusters = []
    used = set()

    for i, a in enumerate(fingerprints):
        if i in used:
            continue

        cluster = [a]
        used.add(i)

        for j, b in enumerate(fingerprints):
            if j in used:
                continue

            if (
                a["avg_gap_seconds"] is not None
                and b["avg_gap_seconds"] is not None
                and abs(a["avg_gap_seconds"] - b["avg_gap_seconds"]) <= time_threshold
            ):
                cluster.append(b)
                used.add(j)

        if len(cluster) > 1:
            clusters.append(cluster)

    return clusters
