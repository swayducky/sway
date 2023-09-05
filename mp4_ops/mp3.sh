#!/bin/bash

# Check for input argument
if [ "$#" -ne 1 ]; then
    echo "Usage: ./mp3.sh <input_video>"
    exit 1
fi

# Extract the input file name and directory
input_file="$1"
directory=$(dirname -- "$input_file")
filename=$(basename -- "$input_file")
extension="${filename##*.}"
filename="${filename%.*}"

# Generate output file name in the same directory as the input file
output_file="${directory}/${filename}.mp3"

# Run FFmpeg to extract audio and save as MP3
ffmpeg -i "$input_file" -q:a 0 -map a "$output_file"

# Check FFmpeg exit status
if [ $? -eq 0 ]; then
    echo "Successfully extracted the audio. Output saved as $output_file"
else
    echo "Failed to extract the audio."
fi
