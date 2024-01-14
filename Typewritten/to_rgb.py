import os
import sys
from PIL import Image


# Helper, convert hex colour to tuple
def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))


def main(directory_path, bgcolor=(255, 255, 255)):
    filenames = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith('.png')]

    for filename in filenames:
        with Image.open(filename) as image:
            if image.mode == 'RGB':
                print("Skipping", filename)
                continue

            # Convert image to RGBA if not already in that mode
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            # Paste old image into new image with default background colour
            background = Image.new('RGB', image.size, bgcolor)
            background.paste(image, mask=image.split()[3])  # 3 is the alpha channel

            filename_without_extension = os.path.splitext(filename)[0]
            new_filename = f'{filename_without_extension}_modified.png'
            background.save(new_filename)
            print("Saved", new_filename)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: to_rgb.py <dir> [bgcolor]")
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print("Directory not found", sys.argv[1])
        sys.exit(1)

    args = sys.argv[1:]
    if len(args) == 2:
        args[1] = hex_to_rgb(args[1])

    main(*args)
