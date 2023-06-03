#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg could not be found. Please install it first."
    exit 1
fi

# Process all MP4 files in the input directory
for input_file in ./_in_video/*.mp4; do
    # Get the base name of the file
    base_name=$(basename "$input_file")

    # Create the output file name
    output_file="./_out/${base_name%.*}_reencoded.mp4"

    # Re-encode the video
    ffmpeg -i "$input_file" -c:v libx264 -crf 23 -c:a aac -strict -2 -movflags +faststart "$output_file"
done

echo "Re-encoding completed. Output files are in the './_out' directory."