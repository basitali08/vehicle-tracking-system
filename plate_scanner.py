"""
License plate scanner using EasyOCR.
Detects and reads plate text from images.
"""
import os
import cv2
import numpy as np
from PIL import Image
import easyocr

reader = None


def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    return reader


def scan_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        pil_img = Image.open(image_path)
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    reader = get_reader()
    results = reader.readtext(img)

    SKIP_WORDS = {'PAKISTAN', 'ISLAMABAD', 'KARACHI', 'LAHORE', 'PESHAWAR', 'QUETTA', 'LINCOLN', 'EUROPE'}

    plates = []
    for bbox, text, confidence in results:
        text = text.strip().upper().replace(' ', '')
        clean = text.replace('-', '')
        if len(clean) >= 4 and clean not in SKIP_WORDS and confidence > 0.3:
            plates.append({
                'plate': text,
                'confidence': round(confidence, 3),
                'bbox': [[int(p[0]), int(p[1])] for p in bbox],
            })

    plates.sort(key=lambda x: x['confidence'], reverse=True)
    return plates


def scan_all_in_directory(directory='samples'):
    results = []
    for fname in sorted(os.listdir(directory)):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(directory, fname)
            detected = scan_image(path)
            for d in detected:
                d['image'] = fname
            results.extend(detected)
    return results


if __name__ == '__main__':
    print("Testing scanner on samples/ ...")
    results = scan_all_in_directory()
    print(f"Detected {len(results)} plates across samples:")
    seen = set()
    for r in results[:20]:
        if r['plate'] not in seen:
            print(f"  {r['plate']:12s} (conf: {r['confidence']:.2f}) [{r['image']}]")
            seen.add(r['plate'])
