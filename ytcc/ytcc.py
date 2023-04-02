import openai
import os
import yt_dlp as youtube_dl
import webvtt
from moviepy.editor import *
import json

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to download the audio from a YouTube video
def download_audio(video_url, output_file):
    print("== Downloading video, then extracting audio...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Function to split the audio file into smaller chunks
def split_audio_file(audio_file_path, chunk_length):
    print("== Splitting audio...")
    audio = AudioFileClip(audio_file_path)
    duration = audio.duration
    chunks = []

    start_time = 0
    while start_time < duration:
        end_time = min(start_time + chunk_length, duration)
        chunk = audio.subclip(start_time, end_time)
        chunk_file = f"chunk_{start_time}-{end_time}.mp3"
        chunk.write_audiofile(chunk_file)
        chunks.append(chunk_file)
        start_time += chunk_length

    return chunks

# Function to transcribe an audio file using the Whisper API
def transcribe_audio(audio_file_path):
    print(f"== Transcribing audio for: {audio_file_path} -- one moment...")
    with open(audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript['text'])
    return transcript['text']

# Function to create a captions file (SRT format)
def create_captions_file(transcript, output_file):
    captions = []
    index = 1

    for item in transcript['results']:
        start_time = item['start']
        end_time = item['end']
        text = item['text']

        caption = {
            'index': index,
            'start': start_time,
            'end': end_time,
            'text': text,
        }

        captions.append(caption)
        index += 1

    with open(output_file, 'w') as f:
        for caption in captions:
            f.write(f"{caption['index']}\n")
            f.write(f"{caption['start']} --> {caption['end']}\n")
            f.write(f"{caption['text']}\n\n")

# Function to get video information from a YouTube URL
def get_video_info(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'nocheckcertificate': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info['title'], info['webpage_url']



    # Function to get video information from a YouTube URL
def get_video_info(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'nocheckcertificate': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info['title'], info['webpage_url']

# Function to download subtitles (CC) from a YouTube video
def download_subtitles(video_url, output_file):
    ydl_opts = {
        'skip_download': True,
        'writeautomaticsub': True,
        'subtitlesformat': 'srt',
        'outtmpl': output_file + '.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            return True
        except youtube_dl.DownloadError:
            return False


def convert_vtt_to_plaintext(vtt_file, similarity_threshold=90):
    captions = webvtt.read(vtt_file)
    plaintext_captions = []
    prev_text = ""

    for caption in captions:
        for line in caption.text.split('\n'):
            line = line.strip()
            if line and line != prev_text:
                print(prev_text, "====>", line)
                plaintext_captions.append(line)
                prev_text = line

    return "\n".join(plaintext_captions)


if __name__ == "__main__":
    # Main script
    video_url = "https://www.youtube.com/watch?v=GRP5rsyO9Pw"
    audio_output = "audio.mp3"
    chunk_length = 60 * 15  # Split audio into 15min chunks

    title, url = get_video_info(video_url)
    print("== Video title:", title)
    print("== URL:", url)

    subtitles_output = "captions.srt"

    title, url = get_video_info(video_url)
    if download_subtitles(video_url, subtitles_output):
        downloaded_subtitles_file = f"{subtitles_output}.en.vtt"  # Use the correct file name
        captions_content = convert_vtt_to_plaintext(downloaded_subtitles_file)

        with open('transcript.txt', "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write(f"URL: {url}\n\n")
            f.write(captions_content)
    else:
        download_audio(video_url, 'audio')
        audio_chunks = split_audio_file(audio_output, chunk_length)
        os.remove(audio_output)


        text_chunks = []
        for audio_chunk in audio_chunks:
            text_chunk = transcribe_audio(audio_chunk)
            text_chunks.append(text_chunk)
            os.remove(audio_chunk)

        with open('transcript.txt', "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write(f"URL: {url}\n\n")
            f.write("\n\n".join(text_chunks))
