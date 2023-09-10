#!/usr/bin/env bash

# Extract the input file name and directory
input_file="$1"
directory=$(dirname -- "$input_file")
filename=$(basename -- "$input_file")
filename="${filename%.*}"

# Create a reversed version of the video
CMD="ffmpeg -i $1 -vf 'reverse' -q:v 1 tmp_reversed.mp4"
echo "== Running: $CMD"
$CMD

# Generate output file name in the same directory as the input file
output_file="${directory}/${filename}_last.png"

# Take the first frame of the reversed video
CMD="ffmpeg -i tmp_reversed.mp4 -frames:v 1 $output_file"
echo "== Running: $CMD"
$CMD

# Clean up the reversed video
rm tmp_reversed.mp4

echo "== Done! See: $output_file"
