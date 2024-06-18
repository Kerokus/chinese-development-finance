"""
This script takes in a directory of images generated from plotly
and stitches them together into a timeline gif.

Example:
    $ python build_gif.py
"""

import os
import imageio.v2 as imageio


def initialize():
    global input_directory, output_directory, output_filename

    ##### SET FILE LOCATIONS #####
    input_directory = "../img/south-america/gif_frames"
    output_directory = "../img/south-america"
    output_filename = "chinese-loans-south-america-2000-2021.gif"


def create_gif():
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all PNG files in the input directory and sort them by name
    images = sorted([img for img in os.listdir(
        input_directory) if img.endswith(".png")])

    # Create a list to hold the image data
    image_data = []

    # Read each image file and append it to the list
    for img in images:
        image_path = os.path.join(input_directory, img)
        image_data.append(imageio.imread(image_path))

    # Create the GIF
    gif_path = os.path.join(output_directory, output_filename)
    # Adjust the fps value if needed
    imageio.mimsave(gif_path, image_data, fps=1)

    print(f"GIF saved as {gif_path}")


if __name__ == "__main__":
    initialize()
    create_gif()
