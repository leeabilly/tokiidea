#!/usr/bin/env python3
import os
import re

# List of emojis to remove (we can extend)
emojis = ['🧸', '📷', '🎵', '📌', '📘', '💖', '🛒', '️']  # include variation selector
# Also add any other common emojis we might have missed: we can add ranges but we'll keep simple.
# We'll just do a simple replace for each emoji.

def remove_emojis_from_file(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r') as f:
        content = f.read()
    original = content
    for emoji in emojis:
        content = content.replace(emoji, '')
    # Also remove any standalone variation selector that might have been left
    content = content.replace('️', '')
    if content != original:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Removed emojis from {file_path}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = ['index.html', 'product.html', 'contact.html', 'faq.html', 'shipping.html', 'returns.html', 'privacy.html', 'terms.html', 'cookies.html']
    for html_file in html_files:
        html_path = os.path.join(base_dir, html_file)
        remove_emojis_from_file(html_path)
    # Also check any other .html files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html') and file not in html_files:
                remove_emojis_from_file(os.path.join(root, file))

if __name__ == '__main__':
    main()