"""
Generate synthetic Pakistani-style license plate images for the vehicle tracking project.
Pakistani plates follow format: [2-3 letters]-[3-4 digits] (e.g., LEG-456, ISB-1234)
"""
import os
import random
import string
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = 'samples'
NUM_PLATES = 200
PLATE_WIDTH = 400
PLATE_HEIGHT = 120
HOTLIST_RATIO = 0.1  # 10% of generated plates are "hotlisted"

random.seed(42)


def random_plate():
    letters = ''.join(random.choices(string.ascii_uppercase, k=random.randint(2, 3)))
    digits = ''.join(random.choices(string.digits, k=random.randint(3, 4)))
    return f"{letters}-{digits}"


def generate_plate_image(plate_text, save_path):
    img = Image.new('RGB', (PLATE_WIDTH, PLATE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Border
    draw.rectangle([2, 2, PLATE_WIDTH - 3, PLATE_HEIGHT - 3], outline=(0, 51, 102), width=4)

    # Simple clean plate — white background, black text, no distractions
    draw.rectangle([2, 2, PLATE_WIDTH - 3, PLATE_HEIGHT - 3], outline=(0, 51, 102), width=4)

    try:
        font = ImageFont.truetype("arial.ttf", 56)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), plate_text, font=font)
    tw = bbox[2] - bbox[0]
    x = (PLATE_WIDTH - tw) // 2
    y = (PLATE_HEIGHT - (bbox[3] - bbox[1])) // 2
    draw.text((x, y), plate_text, fill=(0, 0, 0), font=font)

    # Thin border at bottom
    draw.rectangle([0, PLATE_HEIGHT - 6, PLATE_WIDTH, PLATE_HEIGHT], fill=(0, 51, 102))

    img.save(save_path)
    return plate_text


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    hotlist_plates = set()
    all_plates = []

    for i in range(NUM_PLATES):
        plate = random_plate()
        filename = f"plate_{i:04d}_{plate}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        generate_plate_image(plate, filepath)
        all_plates.append(plate)

        if i < int(NUM_PLATES * HOTLIST_RATIO):
            hotlist_plates.add(plate)

    print(f"Generated {len(all_plates)} plate images in {OUTPUT_DIR}/")

    with open(os.path.join(OUTPUT_DIR, 'hotlist_plates.txt'), 'w') as f:
        for plate in sorted(hotlist_plates):
            f.write(f"{plate}\n")
    print(f"Hotlisted {len(hotlist_plates)} plates (saved to {OUTPUT_DIR}/hotlist_plates.txt)")

    # Show samples
    print(f"\nSample plates (hotlisted): {sorted(hotlist_plates)[:5]}")
    print(f"Sample plates (normal): {[p for p in all_plates if p not in hotlist_plates][:5]}")
