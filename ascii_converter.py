from PIL import Image, ImageEnhance
import numpy as np
import os

def preprocess_image(image):
    """Enhance image details before conversion"""
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.5)
    
    return image

def get_ascii_char(pixel_value):
    """Get more precise ASCII char mapping"""
    ascii_chars = "@%#*+=-:. "
    ascii_chars = ascii_chars[::-1]
    
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

def save_ascii_art(ascii_art, filename):
    """Save ASCII art with proper encoding in the results directory"""
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    file_path = os.path.join(results_dir, filename)
    
    if not file_path.endswith('.txt'):
        file_path += '.txt'
    
    # Save the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(ascii_art)
    
    return file_path

def get_valid_filename():
    """Get a valid filename from user input"""
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
        
        saved_path = save_ascii_art(ascii_art, filename)
        print(f"ASCII art has been generated and saved as: {saved_path}")
        
        lines = ascii_art.split('\n')
        print(f"Output dimensions: {len(lines[0])} x {len(lines)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

