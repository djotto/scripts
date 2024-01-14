import sys
import glob
import os
import cv2
import numpy as np


def deskew(image):

    # Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Perform a dilation and erosion to close gaps in between letters
    dilated_edges = cv2.dilate(edges, None)
    edges = cv2.erode(dilated_edges, None)

    # Detect points that form a line
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=10, maxLineGap=250)
    if lines is None:
        return None, None

    # Prepare an array to store angles
    angles = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2((y2 - y1), (x2 - x1))*(180/np.pi)
        # We assume our images are almost correct, so any line imore than +/-5 deg from the horizontal can be ignored
        if -5 < angle < 5:
            angles.append(angle)
            # Draw Hough lines on image for debugging
            # cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 3)

    if not angles:
        return None, None

    # Calculate average angle and adjust it to rotate the image
    average_angle = np.mean(angles)

    # Get the image size
    height, width = image.shape[:2]

    # Compute the rotation matrix and perform the rotation
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), average_angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # Return the result
    return rotated_image, abs(average_angle)


def main(directory_path):
    filenames = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith('.png')]

    results = []
    for filename in filenames:
        # Load image
        image = cv2.imread(filename)
        if image is None:
            print("Could not load", filename)
            continue

        print("Processing", filename)

        new_image, average_skew = deskew(image)
        if average_skew is None:
            print("Skipped", filename)
            continue

        new_file = f"{os.path.splitext(filename)[0]}_modified.png"
        cv2.imwrite(new_file, new_image)

        results.append([filename, average_skew])

    # Sort the result by average_skew
    results.sort(key=lambda x: x[1], reverse=True)

    # Print out the ten files with the largest abs(average_angle) so we can manually check them
    for filename, average_skew in results[:10]:
        print(f"filename: {filename}, skew: {average_skew}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: deskew.py <dir>")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print("Directory not found", sys.argv[1])
        sys.exit(1)
    main(sys.argv[1])
