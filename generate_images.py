"""
Beautiful Image Generator for Arabic Learning Videos
Uses ONE pre-made background image for all phrases with RTL Arabic text support
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Image dimensions
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920

# Background image path
BACKGROUND_IMAGE = Path("background.png")

# Arabic font path (using common Arabic fonts)
ARABIC_FONT_PATHS = [
    "fonts/arial.ttf",  # Arial supports Arabic
    "fonts/arabictypesetting.ttf",
    "fonts/scheherazade-new.ttf",
    "fonts/amiri.ttf",
    "C:/Windows/Fonts/arial.ttf",  # Windows system font
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux fallback
]


def create_default_background():
    """
    Create a beautiful default gradient background if none exists
    Arabic/Islamic inspired colors: Green, Gold, Blue
    """

    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(img)

    # Create beautiful gradient (Arabic/Islamic colors: Emerald green to Gold to Deep blue)
    for y in range(IMAGE_HEIGHT):
        ratio = y / IMAGE_HEIGHT

        if ratio < 0.4:
            # Top: Deep emerald green to teal
            r = int(0 + (0) * (ratio / 0.4))
            g = int(100 + (139 - 100) * (ratio / 0.4))
            b = int(60 + (127 - 60) * (ratio / 0.4))
        elif ratio < 0.7:
            # Middle: Teal to gold
            r = int(0 + (255 - 0) * ((ratio - 0.4) / 0.3))
            g = int(139 + (215 - 139) * ((ratio - 0.4) / 0.3))
            b = int(127 + (0 - 127) * ((ratio - 0.4) / 0.3))
        else:
            # Bottom: Gold to deep blue
            r = int(255 + (0 - 255) * ((ratio - 0.7) / 0.3))
            g = int(215 + (0 - 215) * ((ratio - 0.7) / 0.3))
            b = int(0 + (139 - 0) * ((ratio - 0.7) / 0.3))

        draw.rectangle([(0, y), (IMAGE_WIDTH, y + 1)], fill=(r, g, b))

    # Add subtle Islamic geometric pattern (circles and stars)
    for i in range(0, IMAGE_WIDTH, 100):
        for j in range(0, IMAGE_HEIGHT, 100):
            # Draw circles
            draw.ellipse(
                [(i + 30, j + 30), (i + 70, j + 70)],
                outline=(255, 215, 0, 40),  # Gold
                width=2
            )
            # Draw small stars at intersections
            cx, cy = i + 50, j + 50
            for angle in range(0, 360, 45):
                import math
                rad = math.radians(angle)
                x1 = int(cx + 10 * math.cos(rad))
                y1 = int(cy + 10 * math.sin(rad))
                x2 = int(cx + 20 * math.cos(rad))
                y2 = int(cy + 20 * math.sin(rad))
                draw.line([(x1, y1), (x2, y2)], fill=(255, 215, 0, 60), width=2)

    # Save background
    img.save(BACKGROUND_IMAGE, quality=95)
    print(f"[background] ✅ Created default background: {BACKGROUND_IMAGE}")

    return img


def load_background():
    """
    Load the background image (creates default if doesn't exist)
    """

    if not BACKGROUND_IMAGE.exists():
        print("[background] No background found, creating default...")
        return create_default_background()

    return Image.open(BACKGROUND_IMAGE)


def load_arabic_font(font_path, size):
    """Load Arabic font with fallback support"""
    for path in ARABIC_FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    # Last resort: default font
    print(f"[fonts] ⚠️ WARNING: Could not load Arabic font {font_path}!")
    return ImageFont.load_default()


def create_phrase_image(phrase_data: dict, output_path: str):
    """
    Create image using the SAME background for all phrases
    Supports RTL Arabic text
    """

    # Load background (reuse same image every time)
    img = load_background().copy()
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        # Try fonts/ folder first
        font_category = ImageFont.truetype("fonts/arial.ttf", 70)
        font_large = ImageFont.truetype("fonts/arialbd.ttf", 85)
        font_arabic = load_arabic_font("fonts/arial.ttf", 90)  # Larger for Arabic
        font_pronunciation = ImageFont.truetype("fonts/ariali.ttf", 28)
    except:
        try:
            # Windows system fonts
            font_category = ImageFont.truetype("arial.ttf", 70)
            font_large = ImageFont.truetype("arialbd.ttf", 85)
            font_arabic = load_arabic_font("C:/Windows/Fonts/arial.ttf", 90)
            font_pronunciation = ImageFont.truetype("ariali.ttf", 28)
        except:
            # Linux fallback
            font_category = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 85)
            font_arabic = load_arabic_font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 90)
            font_pronunciation = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)

    # Get text
    category = phrase_data.get("category", "Arabic Learning")
    english = phrase_data.get("english", "")
    arabic = phrase_data.get("arabic", "")
    pronunciation = phrase_data.get("pronunciation", "")

    # Helper: wrap text
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    # Draw category at top with IMPRESSIVE styling
    category_text = category.upper()
    category_bbox = draw.textbbox((IMAGE_WIDTH // 2, 180), category_text, font=font_category, anchor="mm")

    # Draw gradient background box for category with glow
    padding = 25

    # Glow effect
    for i in range(min(padding, 15)):
        alpha = int(200 - (i * 10))
        if alpha > 0:
            draw.rectangle(
                [
                    (category_bbox[0] - padding + i, category_bbox[1] - padding + i),
                    (category_bbox[2] + padding - i, category_bbox[3] + padding - i)
                ],
                outline=(0, 100, 0, alpha)  # Green glow
            )

    # Solid background
    draw.rectangle(
        [
            (category_bbox[0] - padding, category_bbox[1] - padding),
            (category_bbox[2] + padding, category_bbox[3] + padding)
        ],
        fill=(20, 40, 20, 220)  # Dark green
    )

    # Draw category text with glow
    for offset in [(2,2), (-2,2), (2,-2), (-2,-2)]:
        draw.text(
            (IMAGE_WIDTH // 2 + offset[0], 180 + offset[1]),
            category_text,
            fill=(0, 100, 0),  # Green glow
            font=font_category,
            anchor="mm"
        )

    draw.text(
        (IMAGE_WIDTH // 2, 180),
        category_text,
        fill=(255, 255, 255),
        font=font_category,
        anchor="mm",
        stroke_width=2,
        stroke_fill=(0, 0, 0)
    )

    # Draw English with solid background
    english_y = 500
    english_lines = wrap_text(english, font_large, IMAGE_WIDTH - 140)

    total_height = len(english_lines) * 100

    # Solid background for English (dark blue)
    box_top = english_y - 70
    box_bottom = english_y + total_height - 20

    draw.rectangle(
        [(70, box_top), (IMAGE_WIDTH - 70, box_bottom)],
        fill=(30, 40, 80)  # Dark blue, solid
    )

    # Draw English text
    for i, line in enumerate(english_lines):
        y_pos = english_y + (i * 100)
        draw.text(
            (IMAGE_WIDTH // 2, y_pos),
            line,
            fill=(255, 255, 255),
            font=font_large,
            anchor="mm",
            stroke_width=5,
            stroke_fill=(0, 0, 0)
        )

    # Draw Arabic with solid background (RTL)
    arabic_y = english_y + (len(english_lines) * 100) + 120
    arabic_lines = wrap_text(arabic, font_arabic, IMAGE_WIDTH - 140)

    total_height = len(arabic_lines) * 110  # More spacing for Arabic

    # Solid background for Arabic (warm brown/gold)
    box_top = arabic_y - 70
    box_bottom = arabic_y + total_height - 20

    draw.rectangle(
        [(70, box_top), (IMAGE_WIDTH - 70, box_bottom)],
        fill=(80, 50, 30)  # Warm brown, solid
    )

    # Draw Arabic text (bright yellow for visibility)
    # Arabic is RTL - PIL handles this automatically with proper fonts
    for i, line in enumerate(arabic_lines):
        y_pos = arabic_y + (i * 110)
        draw.text(
            (IMAGE_WIDTH // 2, y_pos),
            line,
            fill=(255, 255, 0),  # Bright yellow
            font=font_arabic,
            anchor="mm",
            stroke_width=5,
            stroke_fill=(0, 0, 0)
        )

    # Draw pronunciation (subtle, elegant) with WRAPPING
    pronunciation_y = arabic_y + (len(arabic_lines) * 110) + 60
    pronunciation_text = f"[{pronunciation}]"

    # Wrap pronunciation text
    max_pron_width = 700
    pron_lines = wrap_text(pronunciation_text, font_pronunciation, max_pron_width)

    # Calculate total height for all pronunciation lines
    pron_line_height = 35
    total_pron_height = len(pron_lines) * pron_line_height

    # Calculate box dimensions
    box_top = pronunciation_y - 12
    box_bottom = pronunciation_y + total_pron_height + 12

    if box_bottom <= box_top:
        box_bottom = box_top + 40

    if pron_lines:
        first_line_bbox = draw.textbbox((IMAGE_WIDTH // 2, pronunciation_y), pron_lines[0], font=font_pronunciation, anchor="mm")
        box_left = first_line_bbox[0] - 15
        box_right = first_line_bbox[2] + 15
    else:
        box_left = IMAGE_WIDTH // 2 - 100
        box_right = IMAGE_WIDTH // 2 + 100

    # Draw background box
    draw.rectangle(
        [(box_left, box_top), (box_right, box_bottom)],
        fill=(40, 40, 60, 150)
    )

    # Draw each pronunciation line
    for i, pron_line in enumerate(pron_lines):
        y_pos = pronunciation_y + (i * pron_line_height)
        draw.text(
            (IMAGE_WIDTH // 2, y_pos),
            pron_line,
            fill=(200, 200, 220),
            font=font_pronunciation,
            anchor="mm",
            stroke_width=1,
            stroke_fill=(0, 0, 0)
        )

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, quality=95, optimize=True)

    return output_path


def generate_complete_image(phrase_data: dict, output_path: str):
    """
    Generate image with text on the SAME background
    """
    return create_phrase_image(phrase_data, output_path)


if __name__ == "__main__":
    # Test
    test_phrase = {
        "english": "Good morning! How are you?",
        "arabic": "صباح الخير! كيف حالك؟",
        "pronunciation": "Sabaah al-khayr! Kayfa haaluk?",
        "category": "التحيات اليومية"
    }

    output = "test_output/test_image.jpg"
    generate_complete_image(test_phrase, output)
    print(f"\n✅ Test image generated: {output}")
