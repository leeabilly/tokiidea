#!/usr/bin/env python3
import os
import sys
import re
from PIL import Image

def get_dominant_colors(image_path, num_colors=2):
    """Return list of dominant colors as RGB tuples."""
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        # Resize to small for speed
        img = img.resize((150, 150))
        # Get colors and counts
        # Using getcolors which returns (count, (r,g,b)) for images with limited colors
        # If image has many colors, we need to quantize. We'll use getcolors with maxcolors=256*256*256? Not feasible.
        # Instead, we'll convert to P palette with adaptive palette of num_colors and get the palette.
        img_p = img.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
        palette = img_p.getpalette()
        # palette is a list of [r,g,b, r,g,b, ...] length 3*num_colors
        color_counts = img_p.getcolors()
        # color_counts is list of (count, palette_index)
        colors = []
        for count, idx in color_counts:
            r = palette[idx*3]
            g = palette[idx*3+1]
            b = palette[idx*3+2]
            colors.append(((r,g,b), count))
        # Sort by count descending
        colors.sort(key=lambda x: x[1], reverse=True)
        # Return the RGB tuples
        return [color for color, _ in colors[:num_colors]]
    except Exception as e:
        print(f"Error getting dominant colors from {image_path}: {e}")
        return [(255, 255, 255), (255, 255, 255)]

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def lighten_color(rgb, factor=0.2):
    """Lighten color by factor (0-1)."""
    r, g, b = rgb
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return (r, g, b)

def darken_color(rgb, factor=0.2):
    """Darken color by factor (0-1)."""
    r, g, b = rgb
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return (r, g, b)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'images+logo')
    logo_path = os.path.join(images_dir, 'tokiidea prof pic 2.jpg')

    if not os.path.exists(logo_path):
        print(f"Logo not found: {logo_path}")
        return 1

    # Get two dominant colors from logo
    dominant = get_dominant_colors(logo_path, num_colors=2)
    if len(dominant) < 2:
        # fallback
        dominant = [(255, 182, 193), (255, 255, 224)]  # light pink, light yellow
    color1, color2 = dominant[0], dominant[1]
    print(f"Dominant colors from logo: {rgb_to_hex(color1)}, {rgb_to_hex(color2)}")

    # Determine which is pinkish and which is yellowish based on hue? We'll just assign:
    # We'll assume color1 is pink, color2 is yellow (or vice versa). We'll compute a simple "yellowness" = g + b - r? Not.
    # Instead, we'll just use them as is and create a palette.
    # We'll create a set of pastel colors: pastel-pink, pastel-yellow, and neutrals.
    # We'll assign:
    # --pastel-pink: color1 (maybe lighten)
    # --pastel-yellow: color2 (maybe lighten)
    # --pastel-blue: lighten(color1, 0.1)  # just a variation
    # --pastel-green: lighten(color2, 0.1)
    # --pastel-lavender: lighten(blend(color1, color2), 0.1)
    # --neutral-white: lighten(blend(color1, color2), 0.3)  # very light

    def blend(c1, c2, ratio=0.5):
        r = int(c1[0] * ratio + c2[0] * (1 - ratio))
        g = int(c1[1] * ratio + c2[1] * (1 - ratio))
        b = int(c1[2] * ratio + c2[2] * (1 - ratio))
        return (r, g, b)

    pink = lighten_color(color1, 0.1)
    yellow = lighten_color(color2, 0.1)
    pastel_blue = lighten_color(pink, 0.1)
    pastel_green = lighten_color(yellow, 0.1)
    pastel_lavender = lighten_color(blend(pink, yellow, 0.5), 0.1)
    neutral_white = lighten_color(blend(pink, yellow, 0.5), 0.3)

    color_map = {
        '--pastel-pink': rgb_to_hex(pink),
        '--pastel-yellow': rgb_to_hex(yellow),
        '--pastel-blue': rgb_to_hex(pastel_blue),
        '--pastel-green': rgb_to_hex(pastel_green),
        '--pastel-lavender': rgb_to_hex(pastel_lavender),
        '--neutral-white': rgb_to_hex(neutral_white),
    }

    # Update css/style.css
    css_path = os.path.join(base_dir, 'css', 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            css_content = f.read()
        # Replace each variable definition
        for var, hex_val in color_map.items():
            pattern = rf'{var}\s*:\s*#[0-9a-fA-F]{{6}};'
            replacement = f'{var}: {hex_val};'
            if re.search(pattern, css_content, re.IGNORECASE):
                css_content = re.sub(pattern, replacement, css_content, flags=re.IGNORECASE)
                print(f"Updated {var} to {hex_val}")
            else:
                print(f"Warning: could not find pattern for {var}")
        with open(css_path, 'w') as f:
            f.write(f"/* Updated colors from logo */\n{css_content}")
        print(f"Updated {css_path}")
    else:
        print(f"CSS file not found: {css_path}")

    # Update logo size: make logo smaller by adding inline style or CSS class.
    # We'll add a style attribute to the logo img: height: 40px; or max-height: 3rem.
    # We'll update all HTML files where logo appears.
    html_files = ['index.html', 'product.html', 'about.html', 'contact.html', 'faq.html', 'shipping.html', 'returns.html', 'privacy.html', 'terms.html', 'cookies.html']
    for html_file in html_files:
        html_path = os.path.join(base_dir, html_file)
        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                content = f.read()
            # Replace the logo img tag to add style
            # Pattern: <img src="images+logo/tokiidea prof pic 2.jpg" alt="Tokiidea logo">
            # We'll replace with <img src="images+logo/tokiidea prof pic 2.jpg" alt="Tokiidea logo" style="height: 40px;">
            # But we need to preserve any existing style.
            # We'll do: <img([^>]*?)alt="Tokiidea logo"([^>]*)>
            # and insert style before closing >.
            def add_logo_style(match):
                # match group 1 is before alt, group 2 after alt
                before = match.group(1)
                after = match.group(2)
                # If style already present, we might want to adjust, but we'll just add.
                if 'style' not in before and 'style' not in after:
                    # Insert style attribute before the closing >
                    # We'll reconstruct: <img ... alt="..." ... style="height: 40px;">
                    # We'll put style attribute after alt.
                    return f'<img{before}alt="Tokiidea logo"{after} style="height: 40px;">'
                else:
                    # If style exists, replace its value? We'll just keep as is.
                    return match.group(0)
            new_content = re.sub(r'<img([^>]*?)alt="Tokiidea logo"([^>]*)>', add_logo_style, content)
            # Also need to handle case where alt and src order swapped.
            # We'll do a more general replacement: <img[^>]*src="[^"]*tokiidea prof pic 2\.jpg"[^>]*>
            # and add style if not present.
            def add_style_general(match):
                tag = match.group(0)
                if 'style' not in tag:
                    # Insert style before closing >
                    if tag.endswith('/>'):
                        # self-closing
                        return tag[:-2] + ' style="height: 40px;" />'
                    else:
                        # > maybe
                        return tag[:-1] + ' style="height: 40px;">'
                else:
                    return tag
            new_content = re.sub(r'<img[^>]*src="[^"]*tokiidea prof pic 2\.jpg"[^>]*>', add_style_general, new_content)
            if new_content == content:
                print(f"Warning: could not update logo size in {html_file}")
            else:
                with open(html_path, 'w') as f:
                    f.write(new_content)
                print(f"Updated logo size in {html_file}")
        else:
            print(f"HTML file not found: {html_file}")

    # Remove about.html and references to it (if user doesn't want about us)
    # We'll delete about.html file and remove links from HTML files.
    about_path = os.path.join(base_dir, 'about.html')
    if os.path.exists(about_path):
        os.remove(about_path)
        print(f"Removed {about_path}")
    # Remove links to about.html from all HTML files
    for html_file in html_files:
        if html_file == 'about.html':
            continue
        html_path = os.path.join(base_dir, html_file)
        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                content = f.read()
            # Remove any <a> tags that href="about.html" or contain about.html
            # We'll replace the whole anchor tag with empty string? Better to remove the list item or link.
            # We'll do a simple removal of the link text and keep surrounding li? We'll just remove the anchor and leave empty li? We'll instead remove the whole <li> that contains the link.
            # We'll do regex for <li>.*?href="about\.html".*?</li>
            new_content = re.sub(r'<li[^>]*>.*?href=["\']about\.html["\'][^>]*>.*?</li>', '', content, flags=re.DOTALL)
            # Also remove any standalone <a href="about.html">...</a>
            new_content = re.sub(r'<a[^>]*href=["\']about\.html["\'][^>]*>[^<]*</a>', '', new_content)
            # Also remove any <a href="index.html#about">About</a> maybe.
            new_content = re.sub(r'<a[^>]*href=["\']index\.html#about["\'][^>]*>[^<]*</a>', '', new_content)
            if new_content != content:
                with open(html_path, 'w') as f:
                    f.write(new_content)
                print(f"Removed about links from {html_file}")

    # Remove ALL emojis: we'll remove common emoji characters.
    # We'll define a set of emoji ranges from the Unicode emoji list (approx).
    # For simplicity, we'll remove characters in the range U+1F600 to U+1F64F (emoticons), U+1F300–U+1F5FF (misc symbols), U+1F680–U+1F6FF (transport), U+1F1E0–U+1F1FF (flags), U+2600–U+26FF (misc symbols), U+2700–U+27BF (dingbats), U+FE0F (variation selector), U+1F900–U+1F9FF (supplemental symbols), etc.
    # We'll create a regex pattern that matches these ranges.
    # Since Python's re doesn't support Unicode property escapes easily, we'll list the ranges we care about.
    # We'll also remove the specific emojis we saw earlier.
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # misc symbols
        "\U0001F680-\U0001F6FF"  # transport
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002600-\U000026FF"  # misc symbols
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U00002500-\U00002BEF"  # geometric shapes
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F000-\U0000FFFF"  # (placeholder) we'll limit to common emojis
        "]+", flags=re.UNICODE
    )
    # Note: The above pattern may be too broad and remove non-emoji symbols from other languages.
    # We'll instead remove only the emojis we know are present: we saw 🧸📷🎵📌📘💖🛒 and maybe others.
    # Let's do a safer approach: remove the specific emojis we know about plus any that are in the typical emoticon range.
    # We'll use a pattern for common emojis we saw and also the generic emoticon range.
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # misc symbols
        "\U0001F680-\U0001F6FF"  # transport
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002600-\U000026FF"  # misc symbols
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "]+", flags=re.UNICODE
    )
    for html_file in html_files:
        if html_file == 'about.html':
            continue
        html_path = os.path.join(base_dir, html_file)
        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                content = f.read()
            new_content = emoji_pattern.sub('', content)
            # Also remove any variation selectors that might be left
            new_content = new_content.replace('️', '')
            if new_content != content:
                with open(html_path, 'w') as f:
                    f.write(new_content)
                print(f"Removed emojis from {html_file}")

    # Ensure policy pages (returns, privacy, cookies, terms, shipping) are present and have no emojis.
    # We already removed emojis above.
    # We'll also maybe simplify the policy pages to be more concise? We'll leave as is.

    print("Update complete.")
    return 0

if __name__ == '__main__':
    sys.exit(main())