from PIL import Image, ImageDraw
import os, random

os.makedirs('input', exist_ok=True)

for i in range(1, 101):
    img = Image.new('RGB', (2480, 3508), 'white')
    d = ImageDraw.Draw(img)
    # border
    d.rectangle([80, 80, 2400, 3428], outline='black', width=6)
    # random lines to simulate drawings
    for k in range(12):
        x1 = random.randint(120, 2360)
        y1 = random.randint(120, 3368)
        x2 = random.randint(120, 2360)
        y2 = random.randint(120, 3368)
        d.line([x1, y1, x2, y2], fill='black', width=random.randint(2, 6))
    # simple shapes
    for k in range(6):
        x = random.randint(200, 2200)
        y = random.randint(200, 3200)
        r = random.randint(20, 120)
        d.ellipse([x-r, y-r, x+r, y+r], outline='black', width=3)

    img.save(f'input/page_{i:03}.png', 'PNG')

print('Generated 100 test images in input/')
