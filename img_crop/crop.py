# /// script
# dependencies = ["pillow"]
# ///

import sys
import os
from PIL import Image

def crop_to_16_9(image_path, output_filename=None):
    try:
        with Image.open(image_path) as img:
            # Calculate the target aspect ratio (16:9)
            target_ratio = 16 / 9

            # Get the current width and height
            width, height = img.size

            # Calculate the current aspect ratio
            current_ratio = width / height

            if current_ratio > target_ratio:
                # Image is too wide, crop the width
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                right = left + new_width
                img = img.crop((left, 0, right, height))
            elif current_ratio < target_ratio:
                # Image is too tall, crop the height
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                bottom = top + new_height
                img = img.crop((0, top, width, bottom))

            # Get the directory of the input file
            input_dir = os.path.dirname(image_path)
            input_filename = os.path.basename(image_path)
            input_name, input_ext = os.path.splitext(input_filename)

            # If no output filename is specified, create a default one
            if output_filename is None:
                output_filename = f"{input_name}_cropped.png"
                output_format = 'PNG'
            else:
                # Get the output extension
                _, output_ext = os.path.splitext(output_filename)
                output_ext = output_ext.lower()

                # Remove the leading dot from the extension
                output_format = output_ext[1:] if output_ext.startswith('.') else output_ext

            # If output format is empty or not recognized, default to PNG
            if not output_format or output_format not in Image.SAVE:
                output_format = 'PNG'
                output_filename = os.path.splitext(output_filename)[0] + '.png'

            # Combine the input directory with the output filename
            output_path = os.path.join(input_dir, output_filename)

            # Convert to RGB or RGBA based on the output format
            if output_format in ['PNG', 'WEBP']:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
            else:
                if img.mode != 'RGB':
                    img = img.convert('RGB')

            # Save the cropped image
            img.save(output_path, format=output_format)
            print(f"Image cropped and saved as {output_path}")

    except IOError:
        print(f"Cannot open image file: {image_path}")
        sys.exit(1)
    except KeyError:
        print(f"Unsupported image format for output: {output_format}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <input_image> [output_filename]")
        sys.exit(1)

    input_image = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else None

    crop_to_16_9(input_image, output_filename)