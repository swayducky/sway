#!/bin/bash

# Check for input argument
if [ "$#" -ne 1 ]; then
    echo "Usage: ./reverse_video.sh <input_video>"
    exit 1
fi

# Extract the input file name and directory
input_file="$1"
directory=$(dirname -- "$input_file")
filename=$(basename -- "$input_file")
extension="${filename##*.}"
filename="${filename%.*}"

# Generate output file name in the same directory as the input file
output_file="${directory}/${filename}_reversed.${extension}"

# Run FFmpeg to reverse video and audio
ffmpeg -i "$input_file" -vf "reverse" -af "areverse" "$output_file"

# Check FFmpeg exit status
if [ $? -eq 0 ]; then
    echo "Successfully reversed the video. Output saved as $output_file"
else
    echo "Failed to reverse the video."
fi
