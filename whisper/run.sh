set -e
ffmpeg -i ~/Downloads/_in/mi.mp4 -vn -ar 44100 -ac 2 -b:a 192k ~/Downloads/_out/output.wav
mv ~/Downloads/_out/output.wav .
source .venv/bin/activate
whisper output.wav
rm output.wav

