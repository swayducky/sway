from PIL import Image, ImageOps, ImageDraw
import os
from pathlib import Path


def circle_crop(path):
    image = Image.open(path)
    image = image.convert("RGBA")  # Ensure alpha layer

    # Crop in the middle, width-wise and height-wise.
    width, height = image.size
    if width != height:
        min_side = min(width, height)
        left = (width - min_side) / 2
        top = (height - min_side) / 2
        right = (width + min_side) / 2
        bottom = (height + min_side) / 2
        image = image.crop((left, top, right, bottom))

    # Make the image circular
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + image.size, fill=255)

    # Create a new image with the same size as mask, but completely transparent
    result = Image.new('RGBA', image.size, (0, 0, 0, 0))

    # Apply the mask to the image using the composite operation
    result = Image.alpha_composite(result, Image.composite(image, result, mask))
    return result

def process_directory(directory):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                print(file)
                path = os.path.join(subdir, file)
                new_image = circle_crop(path)
                
                # Get the relative path of subdirectory
                rel_path = os.path.relpath(subdir, directory)
                
                # Create corresponding output directory
                output_directory = os.path.join("_out", rel_path)
                os.makedirs(output_directory, exist_ok=True)
                
                base_filename, _ = os.path.splitext(file)  # Get the filename without extension
                new_image.save(os.path.join(output_directory, "circle_" + base_filename + ".png"))


process_directory("_images")
