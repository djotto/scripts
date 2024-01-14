import argparse  
import os  
import sys  
from PIL import Image  
  
  
# Helper, determine if a pixel is "white enough" to be paper  
def is_white(pixel, threshold=200):  
    return sum(pixel) > threshold * 3  
  
  
# Find first non-paper-white pixel top of image.
def find_top_margin(image):  
    pixels = image.load()  
    width, height = image.size  
  
    top_margin = height  
  
    # Scan from top to bottom  
    for y in range(height):  
        for x in range(width):  
            if not is_white(pixels[x, y]):  
                top_margin = y  
                return top_margin  
  
    return top_margin  
  
  
def shift_image_vertical(image, desired_margin=100, default_color=(255, 255, 255)):
    # Find the current top margin  
    current_top_margin = find_top_margin(image)  
    width, height = image.size  
  
    # Create a new blank image with the same size as the original  
    new_image = Image.new('RGB', (width, height), default_color)  
  
    # Calculate how much we need to shift the image  
    shift_amount = desired_margin - current_top_margin  
  
    # Paste the original image onto the new image, shifted by the calculated amount  
    new_image.paste(image, (0, shift_amount))  
  
    return new_image  
  
  
def main(directory_path, margin):
    filenames = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith('.png')]

    for filename in filenames:
        with Image.open(filename) as image:
            new_image = shift_image_vertical(image, margin)
            if new_image is None:
                print("Skipping", filename)
                continue

            filename_without_extension = os.path.splitext(filename)[0]
            new_filename = f'{filename_without_extension}_modified.png'
            new_image.save(new_filename)
            print("Saved", new_filename)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: set_top_margin.py <dir> [margin]")
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print("Directory not found", sys.argv[1])
        sys.exit(1)

    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) == 3 else 150)
