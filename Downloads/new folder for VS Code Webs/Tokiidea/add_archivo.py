#!/usr/bin/env python3
import os
import re

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = ['index.html', 'product.html', 'contact.html', 'faq.html', 'shipping.html', 'returns.html', 'privacy.html', 'terms.html', 'cookies.html']
    # Google Fonts link for Archivo
    archivo_link = '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600&display=swap" rel="stylesheet">'
    for html_file in html_files:
        html_path = os.path.join(base_dir, html_file)
        if not os.path.exists(html_path):
            continue
        with open(html_path, 'r') as f:
            content = f.read()
        # Add link if not present
        if archivo_link not in content:
            # Insert after <head> tag
            new_content = re.sub(r'(<head[^>]*>)', r'\1\n    ' + archivo_link, content, count=1)
            with open(html_path, 'w') as f:
                f.write(new_content)
            print(f"Added Archivo font link to {html_file}")
        else:
            print(f"Archivo font link already present in {html_file}")
    # Update CSS font variables
    css_path = os.path.join(base_dir, 'css', 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            css = f.read()
        # Update --font-heading: include Archivo as first choice
        css = re.sub(r"--font-heading:\s*'[^']*'\s*,\s*'[^']*'\s*,\s*'[^']*'\s*,\s*sans-serif;",
                     "--font-heading: 'Archivo', 'Fredoka', 'Quicksand', 'Nunito', 'system-ui', sans-serif;",
                     css)
        # Update --font-body: include Archivo as first choice
        css = re.sub(r"--font-body:\s*'[^']*'\s*,\s*'[^']*'\s*,\s*'[^']*'\s*,\s*sans-serif;",
                     "--font-body: 'Archivo', 'Fredoka', 'Inter', 'Helvetica Neue', 'Arial', sans-serif;",
                     css)
        with open(css_path, 'w') as f:
            f.write(css)
        print("Updated CSS font variables to include Archivo and Fredoka")
    else:
        print("CSS file not found")
    return 0

if __name__ == '__main__':
    exit(main())