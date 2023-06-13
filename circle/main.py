from PIL import Image, ImageOps, ImageDraw
import os

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

    # Add a border
    border_color = "#0AAD0A"
    border = Image.new("RGB", (result.width + 2, result.height + 2), border_color)
    border.paste(result, (1, 1))
    return border

def process_directory(directory):
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            path = os.path.join(directory, filename)
            new_image = circle_crop(path)
            new_image.save(os.path.join("_out", "circle_" + filename)) # Save new images with a prefix

process_directory("_images")
