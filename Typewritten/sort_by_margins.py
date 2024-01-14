import argparse  
import os  
import sys  
from PIL import Image  
  
  
# Helper, determine if a pixel is "white enough" to be paper  
def is_white(pixel, threshold=200):  
    return sum(pixel) > threshold * 3  
  
  
# Return first non-paper-white pixel left and right of image.
def find_margins(image):  
    pixels = image.load()  
    width, height = image.size  
  
    left_margin = width  
    right_margin = 0  
  
    # Scan from left to right  
    for x in range(width):  
        for y in range(height):  
            if not is_white(pixels[x, y]):  
                left_margin = x  
                break  
        if left_margin < width:  
            break  
  
    # Scan from right to left  
    for x in range(width - 1, -1, -1):  
        for y in range(height):  
            if not is_white(pixels[x, y]):  
                right_margin = x  
                break  
        if right_margin > 0:  
            break  
  
    return left_margin, width - right_margin - 1  
  
  
def main(directory_path):
    filenames = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith('.png')]

    results = []
    for filename in filenames:
        print(f"Loading {filename}")
        with Image.open(filename) as image:
            left_margin, right_margin = find_margins(image)
            total_margin = left_margin + right_margin
            results.append((filename, left_margin, right_margin, total_margin))

    # Sort images based on the sum of left and right margins
    results.sort(key=lambda x: x[3], reverse=False)

    # Display top num images with the largest margins
    for result in results:
        filename, left_margin, right_margin = result[:3]
        target_value = 2050
        initial_value = 2550 - left_margin - right_margin
        percentage_increase = ((target_value - initial_value) / initial_value) * 100
        print(f"{filename} Left margin: {left_margin}, Right margin: {right_margin}, percentage_increase: {percentage_increase}%")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sort_by_margins.py <dir>")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print("Directory not found", sys.argv[1])
        sys.exit(1)
    main(sys.argv[1])
