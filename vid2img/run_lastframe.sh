#!/usr/bin/env bash

# Create a reversed version of the video
CMD="ffmpeg -i $1 -vf 'reverse' -q:v 1 tmp_reversed.mp4"
echo "== Running: $CMD"
$CMD

# Take the first frame of the reversed video
CMD="ffmpeg -i tmp_reversed.mp4 -frames:v 1 _out/last_frame.png"
echo "== Running: $CMD"
$CMD

# Clean up the reversed video
rm tmp_reversed.mp4
