#!/usr/bin/env python3
import os
import re
from PIL import Image

def get_average_color(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    img = img.resize((100, 100))
    pixels = list(img.getdata())
    n = len(pixels)
    r = sum(p[0] for p in pixels) // n
    g = sum(p[1] for p in pixels) // n
    b = sum(p[2] for p in pixels) // n
    return (r, g, b)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def lighten_color(rgb, factor=0.2):
    r, g, b = rgb
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return (r, g, b)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, 'images+logo', 'tokiidea prof pic 2.jpg')
    if not os.path.exists(logo_path):
        print("Logo not found")
        return 1
    avg = get_average_color(logo_path)
    print(f"Average logo color: {rgb_to_hex(avg)}")
    # We'll assume this is pinkish; we'll create a yellow by shifting hue?
    # Instead, let's get two dominant colors using a simple method:
    # We'll resize and get colors via getcolors with maxcolors=256
    img = Image.open(logo_path).convert('RGB')
    img = img.resize((150, 150))
    # Convert to P palette with 2 colors
    img_p = img.convert('P', palette=Image.ADAPTIVE, colors=2)
    palette = img_p.getpalette()
    colors = img_p.getcolors()
    # colors is list of (count, palette_index)
    if not colors:
        print("Could not get colors")
        return 1
    colors.sort(key=lambda x: x[0], reverse=True)
    idx1 = colors[0][1]
    idx2 = colors[1][1] if len(colors) > 1 else idx1
    r1, g1, b1 = palette[idx1*3], palette[idx1*3+1], palette[idx1*3+2]
    r2, g2, b2 = palette[idx2*3], palette[idx2*3+1], palette[idx2*3+2]
    color1 = (r1, g1, b1)
    color2 = (r2, g2, b2)
    print(f"Dominant colors: {rgb_to_hex(color1)}, {rgb_to_hex(color2)}")
    # Assign: pastel-pink = color1 (lighten), pastel-blue = color2 (lighten) [repurpose blue as yellow]
    pink = lighten_color(color1, 0.1)
    yellow = lighten_color(color2, 0.1)
    # For other pastel variables, create lighter variations
    pastel_green = lighten_color(pink, 0.2)  # lighter pink
    pastel_lavender = lighten_color(yellow, 0.2)  # lighter yellow
    neutral_white = lighten_color(((pink[0]+yellow[0])//2, (pink[1]+yellow[1])//2, (pink[2]+yellow[2])//2), 0.3)
    color_map = {
        '--pastel-pink': rgb_to_hex(pink),
        '--pastel-blue': rgb_to_hex(yellow),   # repurpose blue as yellow
        '--pastel-green': rgb_to_hex(pastel_green),
        '--pastel-lavender': rgb_to_hex(pastel_lavender),
        '--neutral-white': rgb_to_hex(neutral_white),
    }
    css_path = os.path.join(base_dir, 'css', 'style.css')
    with open(css_path, 'r') as f:
        css = f.read()
    for var, hex_val in color_map.items():
        pattern = rf'{var}\s*:\s*#[0-9a-fA-F]{{6}};'
        replacement = f'{var}: {hex_val};'
        if re.search(pattern, css, re.IGNORECASE):
            css = re.sub(pattern, replacement, css, flags=re.IGNORECASE)
            print(f"Updated {var} to {hex_val}")
        else:
            print(f"Warning: {var} not found")
    with open(css_path, 'w') as f:
        f.write(css)
    print("CSS updated.")
    return 0

if __name__ == '__main__':
    exit(main())