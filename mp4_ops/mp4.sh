#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./convert_to_mp4.sh <input_video>"
    exit 1
fi

input_file="$1"
directory=$(dirname -- "$input_file")
filename=$(basename -- "$input_file")
filename="${filename%.*}"

output_file="${directory}/${filename}.mp4"
ffmpeg -i "$input_file" -c:v copy -c:a copy "$output_file"
