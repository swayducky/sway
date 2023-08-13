import glob
import yt_dlp as youtube_dl
import webvtt


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


def convert_vtt_to_plaintext(vtt_file):
    captions = webvtt.read(vtt_file)
    plaintext_captions = []
    prev_text = ""
    for caption in captions:
        for line in caption.text.split('\n'):
            line = line.strip()
            if line and line != prev_text:
                plaintext_captions.append(line)
                prev_text = line
    return "\n".join(plaintext_captions)

def get_subtitles(video_url):
    subtitles_output = "captions.srt"
    title, url = get_video_info(video_url)
    if download_subtitles(video_url, subtitles_output):
        downloaded_subtitles_file = glob.glob('*.vtt')[0]
        captions_content = convert_vtt_to_plaintext(downloaded_subtitles_file)

        return f"""Title: {title}\n
URL: {url}

{captions_content}"""


if __name__ == "__main__":
    get_subtitles('https://www.youtube.com/watch?v=5MHglJHYD50')
