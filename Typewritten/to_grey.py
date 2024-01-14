import os
import sys
from PIL import Image


def main(directory_path, bgcolor):
    filenames = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith('.png')]

    for filename in filenames:
        with Image.open(filename) as image:
            if image.mode == 'L':
                print("Skipping", filename)
                continue

            # Convert image to RGBA if not already in that mode
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            # Paste old image into new image with default background colour
            background = Image.new('L', image.size, bgcolor)
            background.paste(image, mask=image.split()[3])  # 3 is the alpha channel

            filename_without_extension = os.path.splitext(filename)[0]
            new_filename = f'{filename_without_extension}_modified.png'
            background.save(new_filename)
            print("Saved", new_filename)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: to_grey.py <dir> [bgcolor]")
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print("Directory not found", sys.argv[1])
        sys.exit(1)

    bgcolor = int(sys.argv[2]) if len(sys.argv) == 3 else 255
    main(sys.argv[1], bgcolor)
