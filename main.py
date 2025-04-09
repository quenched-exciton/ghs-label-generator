import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import messagebox


def generate_ghs_label(chemical_name: str, hazard_symbols: str, container_size: int, output_path='ghs_label.png', font_path='arial.ttf') -> None:
    width, height = 300, 600
    background_color = "white"
    text_color = "black"
    border_color = "black"
    max_symbols = 8

    img = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=border_color, width=3)

    try:
        font = ImageFont.truetype(font_path, 20)
    except IOError:
        print(f"Warning: '{font_path}' not found. Falling back to default font.")
        font = ImageFont.load_default()

    max_text_width = width - 20
    bbox = font.getbbox("A")
    char_width = bbox[2] - bbox[0] if bbox else 10
    wrap_width = max(10, max_text_width // char_width)
    wrapped_text = textwrap.fill(chemical_name, width=wrap_width)
    draw.text((10, 10), wrapped_text, fill=text_color, font=font)

    limited_symbols = hazard_symbols[:max_symbols]
    symbol_area_height = height - 160
    symbol_y = 100
    if limited_symbols:
        symbol_spacing = symbol_area_height // len(limited_symbols)
    else:
        symbol_spacing = 0

    for symbol_filename in limited_symbols:
        symbol_path = os.path.join("ghs_pictograms", symbol_filename)
        try:
            symbol_img = Image.open(symbol_path).resize((50, 50))
            img.paste(symbol_img, (width // 3 - 25, symbol_y))
        except IOError:
            print(f"Warning: Could not load symbol image: {symbol_filename}")
        symbol_y += symbol_spacing

    container_y = height - 40
    if symbol_y >= container_y - 20:
        container_y = symbol_y + 20
        if container_y > height - 20:
            container_y = height - 20
    draw.text((10, container_y), f"Size: {container_size}", fill=text_color, font=font)

    try:
        img.save(output_path)
        print(f"GHS label saved as {output_path}")
    except IOError as e:
        print(f"Error: Unable to save image to {output_path}. {e}")


def open_label_creator() -> None:
    def submit():
        name = chem_name_var.get()
        size = size_var.get()
        selected = [symbol_box.get(i) for i in symbol_box.curselection()]
        if not name or not selected or not size:
            messagebox.showerror("Error", "Please fill in all fields and select at least one symbol.")
            return
        generate_ghs_label(name, selected, size)

    root = tk.Tk()
    root.title("GHS Label Generator")

    tk.Label(root, text="Chemical Name:").pack()
    chem_name_var = tk.StringVar()
    tk.Entry(root, textvariable=chem_name_var).pack()

    tk.Label(root, text="Container Size:").pack()
    size_var = tk.StringVar()
    tk.Entry(root, textvariable=size_var).pack()

    tk.Label(root, text="Select Hazard Symbols:").pack()
    pictogram_files = [f for f in os.listdir("ghs_pictograms") if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    symbol_box = tk.Listbox(root, selectmode=tk.MULTIPLE)
    for pict in pictogram_files:
        symbol_box.insert(tk.END, pict)
    symbol_box.pack()

    tk.Button(root, text="Generate Label", command=submit).pack(pady=10)

    root.mainloop()


# Run the UI
if __name__ == '__main__':
    open_label_creator()
