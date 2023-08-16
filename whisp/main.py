# Adapted from: https://github.com/Majdoddin/nlp/blob/main/Pyannote_plays_and_Whisper_rhymes_v_2_0.ipynb
import json
import whisper
import re
from pydub import AudioSegment
import os
from dotenv import load_dotenv
from pathlib import Path
import locale
import subprocess
import torch

load_dotenv()

locale.getpreferredencoding = lambda: "UTF-8"

Source = 'Youtube'
video_url = "https://www.youtube.com/watch?v=SRgct4c5T5U"
video_path = "_in/blah.mp3"
output_path = "_out/"
output_path = str(Path(output_path))
audio_title = "Sample Order Taking"

from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token=True)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# pipeline.to(device)

print("output_path:", output_path)
os.chdir(output_path)

video_title = ""
video_id = ""

spacermilli = 2000

def prep():
    if Source == "Youtube":
        from yt_dlp import YoutubeDL
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'outtmpl': f"whisp/input",
        }
        with YoutubeDL(options) as ydl: 
            print("Title: " + video_title) # <= Here, you got the video title
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            video_id = info_dict.get('id', None)
            print("Title: " + video_title)
    # pyannote.audio seems to miss the first 0.5 seconds of the audio, and, therefore, we prepend 2000ms
    audio = AudioSegment.silent(duration=spacermilli).append(AudioSegment.from_wav("whisp/input.wav"), crossfade=0)
    audio.export('input_prep.wav', format='wav')

# prep()

dz = pipeline('input_prep.wav')  
with open("diarization.txt", "w") as text_file:
    text_file.write(str(dz))


def millisec(timeStr):
  spl = timeStr.split(":")
  s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
  return s


dzs = open('diarization.txt').read().splitlines()

groups = []
g = []
lastend = 0

for d in dzs:   
  if g and (g[0].split()[-1] != d.split()[-1]):      #same speaker
    groups.append(g)
    g = []
  
  g.append(d)
  
  end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
  end = millisec(end)
  if (lastend > end):       #segment engulfed by a previous segment
    groups.append(g)
    g = [] 
  else:
    lastend = end
if g:
  groups.append(g)
print(*groups, sep='\n')


audio = AudioSegment.from_wav("input_prep.wav")
gidx = -1
for g in groups:
  start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
  end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1]
  start = millisec(start) #- spacermilli
  end = millisec(end)  #- spacermilli
  gidx += 1
  audio[start:end].export(str(gidx) + '.wav', format='wav')
  print(f"group {gidx}: {start}--{end}")



def timeStr(t):
  return '{0:02d}:{1:02d}:{2:06.2f}'.format(round(t // 3600), 
                                                round(t % 3600 // 60), 
                                                    t % 60)

def whisp():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = whisper.load_model('large', device = device)
    for i in range(len(groups)):
        audiof = str(i) + '.wav'
        result = model.transcribe(audio=audiof, language='en', word_timestamps=True)
        with open(str(i)+'.json', "w") as outfile:
            json.dump(result, outfile, indent=4)  

    speakers = {'SPEAKER_00':('Customer', '#e1ffc7', 'darkgreen'), 'SPEAKER_01':('Call Center', 'white', 'darkorange') }
    def_boxclr = 'white'
    def_spkrclr = 'orange'
    html = list("")
    txt = list("")
    gidx = -1
    for g in groups:  
        shift = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
        shift = millisec(shift) - spacermilli #the start time in the original video
        shift=max(shift, 0)
        
        gidx += 1
        
        captions = json.load(open(str(gidx) + '.json'))['segments']

    if captions:
        speaker = g[0].split()[-1]
        boxclr = def_boxclr
        spkrclr = def_spkrclr
        if speaker in speakers:
            speaker, boxclr, spkrclr = speakers[speaker] 
        
        html.append(f'\n');
        html.append('\n')
        html.append(f'{speaker}\n\t\t\t\t')
        
        for c in captions:
            start = shift + c['start'] * 1000.0 
            start = start / 1000.0   #time resolution ot youtube is Second.            
            end = (shift + c['end'] * 1000.0) / 1000.0      
            txt.append(f'[{timeStr(start)} --> {timeStr(end)}] [{speaker}] {c["text"]}\n')
            for i, w in enumerate(c['words']):
                if w == "":
                    continue
                start = (shift + w['start']*1000.0) / 1000.0        
                html.append(f'{w["word"]}')
        html.append('\n')
        html.append(f'\n')

    with open(f"capspeaker.txt", "w", encoding='utf-8') as file:
        s = "".join(txt)
        file.write(s)
        print('captions saved to capspeaker.txt:')
        print(s+'\n')

    with open(f"capspeaker.html", "w", encoding='utf-8') as file:    #TODO: proper html embed tag when video/audio from file
        s = "".join(html)
        file.write(s)
        print('captions saved to capspeaker.html:')
        print(s+'\n')

whisp()
