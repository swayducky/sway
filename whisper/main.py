import sys
from datetime import timedelta
import whisper

def transcribe_audio(path):
    model = whisper.load_model("base") # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']
    print("Transcription complete. Now writing to file.")
    with open('out.srt') as srtFile:
        for segment in segments:
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text']
            segmentId = segment['id']+1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text}\n\n"
            srtFile.write(segment)

if __name__ == "__main__":
    path = sys.argv[1]
    print("Transcribing:", path)
    transcribe_audio(path) # Change this to your desired audio file
