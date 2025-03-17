from PIL import Image, ImageEnhance
import numpy as np
import os
from fpdf import FPDF

def preprocess_image(image):
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.5)
    
    return image

def get_ascii_char(pixel_value):
    # New: " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" (from darkest to lightest)
    # Using a subset focused on the brighter end for better visibility
    ascii_chars = " .:+*=#%@$MW&8B@"  # From darkest to lightest
    
    # Map pixel value to ASCII char
    char_index = int(pixel_value * (len(ascii_chars) - 1))
    return ascii_chars[char_index]

def convert_to_ascii_art(image_path, width=300):
    img = Image.open(image_path)
    
    aspect_ratio = img.height / img.width
    terminal_ratio = 0.5  
    height = int(width * aspect_ratio * terminal_ratio)
    
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    img = preprocess_image(img)
    
    # Convert to grayscale
    img = img.convert('L')
    
    pixels = np.array(img)
    pixels = pixels / 255.0
    
    # Enhance contrast in the pixel values to make bright areas brighter
    pixels = np.power(pixels, 0.8)
    
    for i in range(1, pixels.shape[0] - 1):
        for j in range(1, pixels.shape[1] - 1):
            neighborhood = pixels[i-1:i+2, j-1:j+2]
            local_min = neighborhood.min()
            local_max = neighborhood.max()
            if local_max > local_min:
                pixels[i, j] = (pixels[i, j] - local_min) / (local_max - local_min)
    
    ascii_art = []
    for row in pixels:
        ascii_row = ''.join([get_ascii_char(pixel) for pixel in row])
        ascii_art.append(ascii_row)
    
    return '\n'.join(ascii_art)

def save_as_pdf(ascii_art, filename, inverted=True):
    
    lines = ascii_art.split('\n')
    num_chars_per_line = len(lines[0])
    num_lines = len(lines)
    
    # Create custom PDF class with background color support
    class PDF(FPDF):
        def header(self):
            pass
        
        def footer(self):
            pass
        
        def set_background(self, inverted):
            if inverted:
                # Set pure black background
                self.set_fill_color(0, 0, 0)
                self.rect(0, 0, self.w, self.h, style='F')
    
    # Standard A4 page (portrait by default)
    pdf = PDF(unit='pt', format='A4')  # Using points for more precise control
    pdf.add_page()
    pdf.set_background(inverted)
    
    # A4 dimensions in points (1 pt = 1/72 inch)
    page_width_pt = 595  # 8.27 inches
    page_height_pt = 842  # 11.69 inches
    
    # Set margins (smaller margins to maximize space)
    margin_pt = 20
    pdf.set_margins(margin_pt, margin_pt, margin_pt)
    
    # Calculate available space
    available_width_pt = page_width_pt - 2 * margin_pt
    available_height_pt = page_height_pt - 2 * margin_pt
    
    char_width_to_height_ratio = 0.6
    ascii_width = num_chars_per_line
    ascii_height = num_lines / char_width_to_height_ratio
    ascii_aspect_ratio = ascii_height / ascii_width
    
    # Calculate the maximum font size that will fit the entire ASCII art
    # while maintaining the correct aspect ratio
    if (available_height_pt / available_width_pt) > ascii_aspect_ratio:
        
        font_size = available_width_pt / num_chars_per_line
        
        used_width_pt = available_width_pt
        
        used_height_pt = (num_lines * font_size) / char_width_to_height_ratio * 1.2  # 1.2 for line height
    else:
        
        font_size = (available_height_pt * char_width_to_height_ratio) / num_lines
        
        used_height_pt = available_height_pt
        
        used_width_pt = num_chars_per_line * font_size / 0.6  # 0.6 is char width ratio
    
    # Apply a safety factor to ensure everything fits
    font_size *= 0.9
    used_width_pt *= 0.9
    used_height_pt *= 0.9
    
    # Set font and color
    pdf.set_font("Courier", size=font_size, style='B')  # Added bold style for better visibility
    if inverted:
        pdf.set_text_color(255, 255, 255)
    else:
        pdf.set_text_color(0, 0, 0)
    
    line_height = font_size * 1.2
    
    # Calculate centering offsets for both horizontal and vertical positioning
    x_offset = (available_width_pt - used_width_pt) / 2
    y_offset = (available_height_pt - used_height_pt) / 2
    
    # Set starting position with both horizontal and vertical centering
    x_start = margin_pt + x_offset
    y_start = margin_pt + y_offset
    
    # Position at the starting point
    pdf.set_xy(x_start, y_start)
    
    # Add each line to PDF with proper alignment
    for line in lines:
        line_width_pt = len(line) * font_size * 0.6
        
        x_line_start = margin_pt + (available_width_pt - line_width_pt) / 2
        
        pdf.set_x(x_line_start)
        
        pdf.cell(line_width_pt, line_height, line, ln=True, align='C')
    
    # Save PDF
    pdf_path = os.path.join("results", f"{filename}.pdf")
    pdf.output(pdf_path)
    return pdf_path

def save_ascii_art(ascii_art, filename):
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Save as text file
    txt_path = os.path.join(results_dir, f"{filename}.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(ascii_art)
    
    # Save as PDF with black background and white text
    pdf_path = save_as_pdf(ascii_art, filename, inverted=True)
    
    return txt_path, pdf_path

def get_valid_filename():
    while True:
        filename = input("Enter a name for your ASCII art: ").strip()
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
        
        if filename:
            return filename
        print("Please enter a valid filename (using letters, numbers, spaces, hyphens, or underscores)")

def main():
    try:
        print("Converting image to ASCII art...")
        ascii_art = convert_to_ascii_art("input_image.jpg", width=300)
        
        filename = get_valid_filename()
        
        txt_path, pdf_path = save_ascii_art(ascii_art, filename)
        print(f"ASCII art has been generated and saved as:")
        print(f"- Text file: {txt_path}")
        print(f"- PDF file: {pdf_path} (with black background for better contrast)")
        
        lines = ascii_art.split('\n')
        print(f"Output dimensions: {len(lines[0])} x {len(lines)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

