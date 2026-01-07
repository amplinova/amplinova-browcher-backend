from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from io import BytesIO


def get_initials(title):
    words = title.strip().split()

    if len(words) == 1:
        return words[0][0].upper()

    return (words[0][0] + words[1][0]).upper()



def generate_logo_from_text(text):
    size = (256, 256)
    bg_color = (59, 130, 246)  # Tailwind blue-500
    text_color = (255, 255, 255)

    image = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()

    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

    draw.text(position, text, fill=text_color, font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return ContentFile(buffer.getvalue(), name=f"{text.lower()}_logo.png")
