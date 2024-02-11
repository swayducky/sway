#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: <first_image>"
    exit 1
fi

input_file="$1"
directory=$(dirname -- "$input_file")
filename=$(basename -- "$input_file")
extension="${filename##*.}"
filename="${filename%.*}"

output_file="${directory}/output.mp4"
RESOLUTION=$(identify -format "%wx%h" $input_file)
echo "RESOLUTION detected: $RESOLUTION Extension: ${extension}"
ffmpeg -framerate 25.0 -i $directory/%04d.$extension -vf "scale=$RESOLUTION" -c:v libx264 -r 25 -pix_fmt yuv420p $output_file
echo "See: $output_file"
