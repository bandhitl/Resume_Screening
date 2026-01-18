#!/usr/bin/env python3
"""
Generate PWA icons using PIL/Pillow.
Run this script to create app icons for the PWA.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a square icon with the specified size."""
    # Create image with gradient background
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)

    # Add a simple icon design (document with person)
    margin = size // 8
    doc_width = size // 2
    doc_height = size // 1.5

    # Draw document background
    doc_x = (size - doc_width) // 2
    doc_y = (size - doc_height) // 2
    draw.rectangle([doc_x, doc_y, doc_x + doc_width, doc_y + doc_height],
                   fill='white', outline='white', width=2)

    # Draw person icon
    head_radius = size // 10
    center_x = size // 2
    head_y = doc_y + doc_height // 3
    draw.ellipse([center_x - head_radius, head_y - head_radius,
                  center_x + head_radius, head_y + head_radius],
                 fill='#667eea')

    # Draw body
    body_width = size // 5
    body_height = size // 5
    body_y = head_y + head_radius + 5
    draw.rectangle([center_x - body_width // 2, body_y,
                    center_x + body_width // 2, body_y + body_height],
                   fill='#667eea')

    img.save(output_path, 'PNG')
    print(f'Created {output_path} ({size}x{size})')


def main():
    """Generate all required icon sizes."""
    sizes = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512]
    icons_dir = 'static/icons'

    # Create icons directory if it doesn't exist
    os.makedirs(icons_dir, exist_ok=True)

    print('Generating PWA icons...')
    for size in sizes:
        output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        create_icon(size, output_path)

    print(f'\nAll icons generated successfully in {icons_dir}/')


if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print('Error: Pillow library not found.')
        print('Install it with: pip install Pillow')
        print('\nAlternatively, you can use online tools to generate icons:')
        print('- https://realfavicongenerator.net/')
        print('- https://www.pwabuilder.com/imageGenerator')
