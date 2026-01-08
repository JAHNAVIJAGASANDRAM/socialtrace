import imagehash

def compare_phashes(hashes1, hashes2, threshold=8):
    matches = 0

    for h1 in hashes1:
        for h2 in hashes2:
            if imagehash.hex_to_hash(h1) - imagehash.hex_to_hash(h2) <= threshold:
                matches += 1

    return matches > 2
