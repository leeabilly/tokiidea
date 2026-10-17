#!/usr/bin/env python3
import os
import sys
from PIL import Image
import json
import re
import shutil

def get_average_color(image_path):
    """Return average color as (r, g, b) from 0-255."""
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        # Resize to small size for faster processing
        img = img.resize((100, 100))
        pixels = list(img.getdata())
        n = len(pixels)
        r = sum(p[0] for p in pixels) // n
        g = sum(p[1] for p in pixels) // n
        b = sum(p[2] for p in pixels) // n
        return (r, g, b)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return (0, 0, 0)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'images+logo')
    if not os.path.isdir(images_dir):
        print(f"Directory {images_dir} not found")
        return 1

    # Find tokiidea prof images
    prof_images = []
    for f in os.listdir(images_dir):
        if f.lower().startswith('tokiidea prof') and f.lower().endswith('.jpg'):
            prof_images.append(os.path.join(images_dir, f))

    if not prof_images:
        print("No tokiidea prof images found")
        return 1

    print(f"Found {len(prof_images)} tokiidea prof images")

    # Compute average colors
    colors = []
    for img_path in prof_images:
        avg = get_average_color(img_path)
        colors.append(avg)
        print(f"{os.path.basename(img_path)}: {rgb_to_hex(avg)}")

    # For simplicity, we'll use the first image's color as pastel pink,
    # second as pastel blue, etc. But we need to map to existing variables.
    # Let's just sort by luminance and assign to pastel colors.
    def luminance(rgb):
        r, g, b = rgb
        return 0.299*r + 0.587*g + 0.114*b

    colors_sorted = sorted(colors, key=luminance)
    # We'll assign to: pastel-pink, pastel-blue, pastel-green, pastel-lavender, neutral-white
    # But we have only 5 pastel variables; we'll map first 5.
    variable_names = ['--pastel-pink', '--pastel-blue', '--pastel-green', '--pastel-lavender', '--neutral-white']
    # Ensure we have at least 5 colors
    if len(colors_sorted) < 5:
        # duplicate last
        while len(colors_sorted) < 5:
            colors_sorted.append(colors_sorted[-1])

    color_map = {}
    for var, rgb in zip(variable_names, colors_sorted[:5]):
        color_map[var] = rgb_to_hex(rgb)

    # Also compute accent colors maybe from other images? We'll keep existing accent-sage and accent-rose for now.
    # But we could also compute from slikica images? We'll leave as is.

    print("Color mapping:")
    for var, hex_val in color_map.items():
        print(f"  {var}: {hex_val}")

    # Update css/style.css
    css_path = os.path.join(base_dir, 'css', 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            css_content = f.read()

        # Replace each variable definition
        for var, hex_val in color_map.items():
            # Pattern: --var: #xxxxxx;
            # We'll replace the line that contains the variable definition.
            # Since the file uses :root { ... }
            # We'll do a simple regex replacement.
            pattern = rf'{var}\s*:\s*#[0-9a-fA-F]{{6}};'
            replacement = f'{var}: {hex_val};'
            if re.search(pattern, css_content, re.IGNORECASE):
                css_content = re.sub(pattern, replacement, css_content, flags=re.IGNORECASE)
                print(f"Updated {var} to {hex_val}")
            else:
                print(f"Warning: could not find pattern for {var}")

        # Write back
        with open(css_path, 'w') as f:
            f.write(css_content)
        print(f"Updated {css_path}")
    else:
        print(f"CSS file not found: {css_path}")

    # Update logo in HTML files: replace text logo with image logo
    logo_img_path = os.path.join('images+logo', 'tokiidea prof pic 2.jpg')
    # We'll need to update index.html, product.html, about.html, contact.html, etc.
    html_files = ['index.html', 'product.html', 'about.html', 'contact.html', 'faq.html', 'shipping.html', 'returns.html', 'privacy.html', 'terms.html', 'cookies.html']
    for html_file in html_files:
        html_path = os.path.join(base_dir, html_file)
        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                content = f.read()
            # Replace the logo link: <a href="index.html" class="logo">Tokiidea</a>
            # We'll replace with <a href="index.html" class="logo"><img src="images+logo/tokiidea prof pic 2.jpg" alt="Tokiidea logo"></a>
            # But we need to preserve the href attribute (might be index.html or relative).
            # We'll do a regex to replace the logo anchor.
            # Pattern: <a[^>]*class="logo"[^>]*>[^<]*</a>
            # We'll replace with the image version, keeping the same href and class.
            def replace_logo(match):
                # match group 0 is the whole anchor tag
                # We'll keep the attributes inside the a tag, replace inner content with img tag.
                inner = match.group(0)
                # Extract the opening tag attributes
                # We'll just replace the whole thing with <a ...><img src="logo" alt="Tokiidea logo"></a>
                # But we need to keep the href etc.
                # Simpler: replace the content between > and <
                # We'll do: <a class="logo" href="...">Tokiidea</a> -> <a class="logo" href="..."><img src="logo" alt="Tokiidea logo"></a>
                # We'll use regex to substitute the inner text.
                return re.sub(r'>[^<]*<', '><img src="' + logo_img_path + '" alt="Tokiidea logo"><', inner, count=1)

            new_content = re.sub(r'<a[^>]*class="logo"[^>]*>[^<]*</a>', replace_logo, content)
            if new_content == content:
                # Maybe the logo is just text without class? Let's try another pattern.
                # Look for <a href="index.html" class="logo">Tokiidea</a> specifically.
                new_content = re.sub(r'<a[^>]*href="[^"]*index\.html"[^>]*class="logo"[^>]*>Tokiidea</a>',
                                     r'<a href="index.html" class="logo"><img src="' + logo_img_path + '" alt="Tokiidea logo"></a>',
                                     content)
            if new_content == content:
                # Fallback: replace the text "Tokiidea" inside anchor with class logo
                new_content = re.sub(r'(<a[^>]*class="logo"[^>]*>)Tokiidea(</a>)',
                                     r'\1<img src="' + logo_img_path + '" alt="Tokiidea logo">\2',
                                     content)
            if new_content == content:
                print(f"Warning: could not replace logo in {html_file}")
            else:
                with open(html_path, 'w') as f:
                    f.write(new_content)
                print(f"Updated logo in {html_file}")
        else:
            print(f"HTML file not found: {html_file}")

    # Add Google Fonts link to each HTML head
    google_fonts_link = '<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap" rel="stylesheet">'
    for html_file in html_files:
        html_path = os.path.join(base_dir, html_file)
        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                content = f.read()
            # Insert after opening <head> tag or before closing </head>
            # We'll insert after <head> if not already present.
            if google_fonts_link not in content:
                # Insert after <head> tag
                new_content = re.sub(r'(<head[^>]*>)', r'\1\n    ' + google_fonts_link, content, count=1)
                with open(html_path, 'w') as f:
                    f.write(new_content)
                print(f"Added Google Fonts link to {html_file}")
            else:
                print(f"Google Fonts link already present in {html_file}")
        else:
            print(f"HTML file not found: {html_file}")

    # Update CSS to use Fredoka font for headings and body
    # We'll modify the :root font-family variables.
    # We'll replace --font-heading and --font-body to include Fredoka.
    # But we want to keep fallback.
    # Let's update css/style.css again.
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            css_content = f.read()
        # Replace --font-heading: 'Quicksand', 'Nunito', 'system-ui', sans-serif;
        # with --font-heading: 'Fredoka', 'Quicksand', 'Nunito', 'system-ui', sans-serif;
        # Similarly for --font-body: 'Fredoka', 'Inter', 'Helvetica Neue', 'Arial', sans-serif;
        css_content = re.sub(r"--font-heading:\s*'[^']*'\s*,\s*'[^']*'\s*,\s*'[^']*'\s*,\s*sans-serif;",
                             "--font-heading: 'Fredoka', 'Quicksand', 'Nunito', 'system-ui', sans-serif;",
                             css_content)
        css_content = re.sub(r"--font-body:\s*'[^']*'\s*,\s*'[^']*'\s*,\s*'[^']*'\s*,\s*sans-serif;",
                             "--font-body: 'Fredoka', 'Inter', 'Helvetica Neue', 'Arial', sans-serif;",
                             css_content)
        with open(css_path, 'w') as f:
            f.write(css_content)
        print("Updated font variables to include Fredoka")

    # Update product.html to showcase Kori product with slikica images
    # We'll find slikica images in images+logo
    slikica_images = []
    for f in os.listdir(images_dir):
        if 'slikica' in f.lower() and f.lower().endswith('.jpg'):
            slikica_images.append(os.path.join(images_dir, f))
    print(f"Found {len(slikica_images)} slikica images")

    # We'll update product.html to replace the main product image and maybe add a gallery.
    # For simplicity, we'll replace the main product image div with a slikica image.
    # We'll also change product title to "Kori".
    product_path = os.path.join(base_dir, 'product.html')
    if os.path.exists(product_path):
        with open(product_path, 'r') as f:
            content = f.read()

        # Change product title
        content = re.sub(r'<h1 class="product-title">[^<]*</h1>',
                         f'<h1 class="product-title">Kori</h1>',
                         content)

        # Replace the main product image div (the one with height: 500px; background-color: var(--neutral-light);)
        # We'll replace the inner div that contains the placeholder emoji with an img tag.
        # Pattern: <div class="product-image" style="height: 500px; background-color: var\((--neutral-light)\); margin-bottom: var\((--spacing-md)\);">
        # Followed by a div with emoji.
        # We'll replace that whole inner div with an img tag.
        # We'll use the first slikica image as main.
        if slikica_images:
            main_img = os.path.join('images+logo', os.path.basename(slikica_images[0]))
            # Replace the div with id? We'll do a regex to replace the content of the product-image div.
            # We'll replace: <div class="product-image" style="height: 500px; background-color: var(--neutral-light); margin-bottom: var(--spacing-md);">.*?</div>
            # with: <div class="product-image" style="height: 500px; background-color: var(--neutral-light); margin-bottom: var(--spacing-md);"><img src="main_img" alt="Kori" style="width:100%;height:100%;object-fit:contain;"></div>
            # We'll do it stepwise.
            # First, find the div and replace its inner content.
            def replace_product_image(match):
                # match group 0 is the whole div
                # We'll keep the opening tag, replace inner content with img tag.
                opening = match.group(1)  # the whole opening tag up to >
                # We'll just replace everything between > and </div>
                return opening + f'><img src="{main_img}" alt="Kori" style="width:100%;height:100%;object-fit:contain;"></div>'

            new_content = re.sub(r'(<div class="product-image" style="height: 500px; background-color: var\((--neutral-light)\); margin-bottom: var\((--spacing-md)\);">).*?(</div>)',
                                 replace_product_image,
                                 content,
                                 flags=re.DOTALL)
            if new_content == content:
                # Try a simpler pattern
                new_content = re.sub(r'(<div class="product-image"[^>]*>).*?(</div>)',
                                     lambda m: m.group(1) + f'><img src="{main_img}" alt="Kori" style="width:100%;height:100%;object-fit:contain;"></div>' + m.group(2),
                                     content,
                                     flags=re.DOTALL)
            if new_content == content:
                print("Warning: could not replace product image in product.html")
            else:
                with open(product_path, 'w') as f:
                    f.write(new_content)
                print("Updated product.html with Kori title and main image")
        else:
            print("No slikica images found for product")

        # Also we might want to update the related products section to show more slikica images? We'll leave as is.
    else:
        print(f"Product.html not found: {product_path}")

    # Remove emojis from all HTML files
    # Emojis are non-ASCII characters; we'll replace common emojis we know about.
    # We'll just remove any characters in the emoji range? Simpler: replace specific emojis we saw.
    # We saw: 🧸, 📷, 🎵, 📌, 📘, 💖, 🛒 (cart icon is also emoji)
    # We'll replace them with empty string or maybe with a simple icon like a letter? We'll just remove.
    emoji_pattern = re.compile(r'[🧸📷🎵📌📘💖🛒]', flags=re.UNICODE)
    for html_file in html_files:
        html_path = os.path.join(base_dir, html_file)
        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                content = f.read()
            new_content = emoji_pattern.sub('', content)
            # Also remove any leftover spaces? We'll leave as is.
            if new_content != content:
                with open(html_path, 'w') as f:
                    f.write(new_content)
                print(f"Removed emojis from {html_file}")
        else:
            print(f"HTML file not found: {html_file}")

    # Also remove emojis from CSS file? Probably none.
    # Done.
    return 0

if __name__ == '__main__':
    sys.exit(main())