# Adapted from: https://github.com/Majdoddin/nlp/blob/main/Pyannote_plays_and_Whisper_rhymes_v_2_0.ipynb

import glob
import sys
import json
import whisper
import re
from pydub import AudioSegment
import os
from dotenv import load_dotenv
import torch
from pathlib import Path
from datetime import timedelta

load_dotenv()

cwd = '_out/bios'
Path(cwd).mkdir(parents=True, exist_ok=True)
os.chdir(cwd)

PREFIX_MILLIS = 2000

def dl_audio():
    video_url = "https://www.youtube.com/watch?v=QAAfDQx8DDQ"
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    from yt_dlp import YoutubeDL
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': "whisp",
        'writeautomaticsub': True,
        'subtitlesformat': 'srt',
    }
    with YoutubeDL(options) as ydl: 
        info_dict = ydl.extract_info(video_url, download=True)
        video_title = info_dict.get('title', None)
        print("Title: " + video_title)

# dl_audio()

def get_audio_file():
    audio_files = [file for ext in ['mp3', 'wav', 'm4a'] for file in glob.glob(f"*.{ext}")]
    print("== audio files found:", audio_files, "=>", audio_files[0])
    return audio_files[0]


def make_lab():
    # pyannote.audio seems to miss the first 0.5 seconds of the audio, and, therefore, we prepend 2000ms
    audio = AudioSegment.silent(duration=PREFIX_MILLIS).append(AudioSegment.from_file(get_audio_file()), crossfade=0)
    audio.export('whisp_tmp.wav', format='wav')
    from pyannote.audio import Pipeline
    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token=True)
    dz = pipeline('whisp_tmp.wav')
    # delete tmp file
    os.remove('whisp_tmp.wav')
    PREFIX_SECONDS = PREFIX_MILLIS / 1000
    windows = []
    with open("dz.lab", "w") as f:
        window = dict(start=PREFIX_SECONDS, end=PREFIX_SECONDS, speaker=None)
        def write(new_turn=None):
            w = dict(start=window['start'] - PREFIX_SECONDS,
                     end=(min(window['end'], new_turn.start) if new_turn else window['end']) - PREFIX_SECONDS,
                     speaker=window['speaker'])
            windows.append(w)
            f.write(f"{w['start']:.3f} {w['end']:.3f} {window['speaker']}\n")
        for turn, track, speaker in dz.itertracks(yield_label=True):
            if speaker != window['speaker']:
                if window['speaker'] is not None:
                    write(turn)
                window['speaker'] = speaker
                window['start'] = turn.start
            window['end'] = turn.end
        write()

# make_lab()

def make_windows():
    windows = []
    with open("dz.lab") as f:
        for line in f:
            start, end, speaker = line.strip().split()
            windows.append({
                'start': float(start),
                'end': float(end),
                'speaker': speaker
            })
    return windows

windows = make_windows()

def timestamp_to_seconds(timestamp):
    hours, minutes, seconds = map(float, timestamp.split(':'))
    return hours * 3600 + minutes * 60 + seconds

def parse_vtt():
    with open(glob.glob("*.vtt")[0], 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content by newline characters to iterate through the lines
    lines = content.strip().split('\n')

    chunks = []
    current_chunk = {}
    for line in lines:
        # Skip lines with metadata
        if line.startswith('WEBVTT') or line.startswith('NOTE'):
            continue
        # If it's an empty line, it indicates the end of the current chunk
        elif line.strip() == '':
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = {}
        # Extract timestamps
        elif re.match(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, end_time = line.split(' --> ')
            current_chunk['start'] = timestamp_to_seconds(start_time)
            current_chunk['end'] = timestamp_to_seconds(end_time)
        # Anything else is assumed to be part of the text
        else:
            current_chunk['text'] = current_chunk.get('text', '') + ' ' + line.strip()

    return chunks

chunks = parse_vtt()

def make_transcript_whisper(windows):
    model = whisper.load_model("base") # Change this to your desired model
    print("Whisper model loaded.")
    result = model.transcribe(audio=get_audio_file(), word_timestamps=True)
    with open('whisp.json', 'w') as jsonFile:
        json.dump(result, jsonFile, indent=2)
    segments = result['segments']
    print("Transcription complete. Now writing to file.")
    index = 0
    last_speaker = None
    with open('whisp.txt', 'w') as f:
        for segment in segments:
            for word in segment['words']:
                while word['start'] >= windows[index]['end']:
                    if index < len(windows) - 1:
                        index += 1
                    else:
                        break
                speaker = windows[index]['speaker']
                if speaker != last_speaker:
                    f.write(f"\n\n[{speaker}] ")
                    last_speaker = speaker
                f.write(word['word'])

# make_transcript_whisper(windows)


def make_transcript(windows, chunks):
    index = 0
    last_speaker = None
    with open('whisp.txt', 'w') as f:
        for chunk in chunks:
            words = chunk['text'].split()
            for i, word in enumerate(words):
                word_start = (chunk['end'] - chunk['start']) * (i / len(words)) + chunk['start']
                while word_start >= windows[index]['end']:
                    if index < len(windows) - 1:
                        index += 1
                    else:
                        break
                speaker = windows[index]['speaker']
                if speaker != last_speaker:
                    f.write(f"\n\n[{speaker}] ")
                    last_speaker = speaker
                f.write(word)


make_transcript(windows, chunks)
