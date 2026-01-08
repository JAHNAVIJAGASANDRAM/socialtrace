from PIL import Image
import imagehash
import cv2
import os

def generate_video_phash(video_path: str):
    cap = cv2.VideoCapture(video_path)
    hashes = []

    frame_count = 0
    while frame_count < 10:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)

        phash = imagehash.phash(img)
        hashes.append(str(phash))

        frame_count += 1

    cap.release()
    return hashes
