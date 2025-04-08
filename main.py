from PIL import Image, ImageDraw, ImageFont
import textwrap

def generate_ghs_label(chemical_name, hazard_symbols, container_size, output_path='ghs_label.png', font_path='arial.ttf'):
    """
    Generates a 300x600 pixel GHS label with customizable chemical name, GHS hazard symbols, and container size.

    :param chemical_name: Name of the chemical
    :param hazard_symbols: List of hazard symbols (as text or Unicode emoji placeholders)
    :param container_size: Size of the container (e.g., '500 mL')
    :param output_path: Path to save the generated PNG file
    :param font_path: Path to the font file to use for rendering text
    """
    width, height = 300, 600
    background_color = "white"
    text_color = "black"
    border_color = "black"
    max_symbols = 8  # Maximum number of symbols that fit without overlap

    img = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Draw border
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=border_color, width=3)

    # Load font
    try:
        font = ImageFont.truetype(font_path, 20)
    except IOError:
        print(f"Warning: '{font_path}' not found. Falling back to default font.")
        font = ImageFont.load_default()

    # Title: Chemical Name
    max_text_width = width - 20  # Adjust based on available space
    bbox = font.getbbox("A")
    char_width = bbox[2] - bbox[0] if bbox else 10
    wrap_width = max(10, max_text_width // char_width)  # Ensure a reasonable wrap width
    wrapped_text = textwrap.fill(chemical_name, width=wrap_width)
    draw.text((10, 10), wrapped_text, fill=text_color, font=font)

    # Hazard Symbols
    limited_symbols = hazard_symbols[:max_symbols]  # Limit number of symbols to avoid overlap
    symbol_area_height = height - 160  # Deduct space for title and container size
    if limited_symbols:
        symbol_spacing = symbol_area_height // len(limited_symbols)
    else:
        symbol_spacing = 0
    symbol_y = 100
    for symbol in limited_symbols:
        draw.text((width // 3, symbol_y), symbol, fill="red", font=font)
        symbol_y += symbol_spacing

    # Container Size - check if it overlaps with last symbol
    container_y = height - 40
    if symbol_y >= container_y - 20:  # 20 is an approximate font height buffer
        container_y = symbol_y + 20
        if container_y > height - 20:
            container_y = height - 20
    draw.text((10, container_y), f"Size: {container_size}", fill=text_color, font=font)

    # Save Image
    try:
        img.save(output_path)
        print(f"GHS label saved as {output_path}")
    except IOError as e:
        print(f"Error: Unable to save image to {output_path}. {e}")
