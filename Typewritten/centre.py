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
  
  
# If offset is negative, move image left. If positive, move right.
def shift_image_horizontal(image, offset, default_color=(255, 255, 255)):  
    width, height = image.size  
  
    # Create a new image with the default background color  
    new_image = Image.new('RGB', (width, height), default_color)  
  
    # Calculate the coordinates for pasting the original image onto the new image  
    if offset < 0:
        # Shift left
        paste_coords = (0, 0, width + offset, height)
        crop_coords = (-offset, 0, width, height)
    else:
        # Shift right  
        paste_coords = (offset, 0, width, height)  
        crop_coords = (0, 0, width - offset, height)  

    # Crop and paste the original image onto the new image  
    cropped_image = image.crop(crop_coords)
    new_image.paste(cropped_image, paste_coords)  
  
    return new_image
  
  
# Centre text block on page
def centre(image):
    left_margin, right_margin = find_margins(image)

    # Close enough
    if abs(left_margin - right_margin) <= 2:
        return None, None, left_margin, right_margin

    if left_margin < right_margin:
        # move right (positive)
        offset = int((right_margin - left_margin) / 2)  
    else:
        # move left (negative)
        offset = -int((left_margin - right_margin) / 2)

    image = shift_image_horizontal(image, offset)

    return image, offset, left_margin, right_margin
  

def main(directory_path):
    filenames = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith('.png')]

    for filename in filenames:
        with Image.open(filename) as image:
            new_image, offset, left_margin, right_margin = centre(image)
            if new_image is None:
                print("Skipping", filename)
                continue

            filename_without_extension = os.path.splitext(filename)[0]
            new_filename = f'{filename_without_extension}_modified.png'
            new_image.save(new_filename)
            print("Saved", new_filename)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: centre.py <dir>")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print("Directory not found", sys.argv[1])
        sys.exit(1)
    main(sys.argv[1])
