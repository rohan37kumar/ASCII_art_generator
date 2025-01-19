# ASCII Art Generator

A Python-based image to ASCII art converter that transforms regular images into detailed ASCII art with enhanced contrast and sharpness. The program includes local contrast enhancement and proper aspect ratio handling for better output quality.

## Features

- Converts images to high-detail ASCII art
- Maintains proper aspect ratio considering terminal character dimensions
- Enhanced image processing:
  - Contrast enhancement
  - Sharpness adjustment
  - Local contrast optimization
- Custom file naming for each generated artwork
- Organized storage in a dedicated results directory
- UTF-8 encoding support
- Input validation for filenames

## Prerequisites

The script requires the following Python libraries:
- PIL (Python Imaging Library)
- NumPy

You can install the required packages using pip:
```bash
pip install Pillow numpy
```

## Project Structure

```
ascii-art-generator/
│
├── input_image.jpg    # Your source image
├── results/           # Directory where ASCII art files are saved
└── ascii_art.py       # Main script
```

## How It Works

1. **Image Preprocessing**
   - Resizes the image while maintaining aspect ratio
   - Enhances contrast and sharpness
   - Converts to grayscale

2. **ASCII Conversion**
   - Maps pixel values to ASCII characters
   - Uses an extended set of ASCII characters for better detail
   - Applies local contrast enhancement for improved definition

3. **Output Handling**
   - Prompts for a custom filename
   - Sanitizes filename input
   - Saves the result in the 'results' directory
   - Automatically adds .txt extension if needed

## Usage

1. Place your input image in the project directory as "input_image.jpg"
2. Run the script:
   ```bash
   python ascii_art.py
   ```
3. When prompted, enter a name for your ASCII art
4. Find your generated ASCII art in the 'results' directory

## Technical Details

- Default output width: 300 characters
- ASCII character set: " .:-=+*#%@" (from lightest to darkest)
- Terminal aspect ratio compensation: 0.5 (accounts for terminal font dimensions)
- Local contrast enhancement using 3x3 pixel neighborhoods
- Image processing parameters:
  - Contrast enhancement: 1.2x
  - Sharpness enhancement: 1.5x

## Final Note
This is just a fun project I decided to create a day before my Web Technology Final Exam. Also took the help of claude to refine the mechanics...

- kc
