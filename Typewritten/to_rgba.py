import os
import sys
from PIL import Image


def main(directory_path):
    filenames = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith('.png')]

    for filename in filenames:
        with Image.open(filename) as image:
            if image.mode == 'RGBA':
                print("Skipping", filename)
                continue

            image = image.convert('RGBA')
            if image is None:
                print("Could not convert", filename)
                continue

            filename_without_extension = os.path.splitext(filename)[0]
            new_filename = f'{filename_without_extension}_modified.png'
            image.save(new_filename)
            print("Saved", new_filename)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: to_rgba.py <dir>")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print("Directory not found", sys.argv[1])
        sys.exit(1)
    main(sys.argv[1])
