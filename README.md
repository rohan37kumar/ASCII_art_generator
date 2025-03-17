# ASCII Art Generator

A Python-based image to ASCII art converter that transforms regular images into detailed ASCII art with enhanced contrast and sharpness. The program includes local contrast enhancement and proper aspect ratio handling for better output quality. The output is provided in both text format and as a high-contrast PDF with black background and optimized character density for maximum visibility.

## Features

- Converts images to high-detail ASCII art
- Maintains proper aspect ratio considering terminal character dimensions
- Enhanced image processing:
  - Contrast enhancement
  - Sharpness adjustment
  - Local contrast optimization
  - Gamma correction for improved brightness
- Optimized character set for maximum visibility on screens
- Multiple output formats:
  - Text file (.txt) for raw ASCII art
  - PDF file with black background and bold white text for optimal viewing
- Custom file naming for each generated artwork
- Organized storage in a dedicated results directory
- UTF-8 encoding support
- Input validation for filenames
- Bold monospace font rendering for improved visibility
- Automatic page size adjustment based on image aspect ratio

## Prerequisites

The script requires the following Python libraries:
- PIL (Python Imaging Library)
- NumPy
- FPDF

You can install the required packages using pip:
```bash
pip install Pillow numpy fpdf
```

## Project Structure

```