import difflib

def linguistic_similarity(text_a, text_b):
    if not text_a or not text_b:
        return 0.0

    return difflib.SequenceMatcher(None, text_a, text_b).ratio()


def analyze_linguistic_patterns(posts):
    """
    posts = list of text captions/comments
    """

    similarities = []

    for i in range(len(posts)):
        for j in range(i + 1, len(posts)):
            score = linguistic_similarity(posts[i], posts[j])
            if score > 0.7:
                similarities.append({
                    "post_a": posts[i],
                    "post_b": posts[j],
                    "similarity": round(score, 2)
                })

    return similarities
