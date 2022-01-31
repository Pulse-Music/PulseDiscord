import pytube
import os

log = lambda msg, level: print(f'[{level}] {msg}')

def search(query):
    log("Searching for " + query + "...",'info')
    yt = pytube.Search(query)
    return yt.results

def download_audio(video: pytube, cwd: str):
    log("Downloading audio...", 'info')
    stream: pytube.Stream = video.streams.filter(only_audio=True).first()
    log(stream.default_filename, 'debug')
    with open(
        os.path.join(
            cwd,
            stream.default_filename.removesuffix(
                '.mp4'
                )
            ),
        'wb'
        ) as f:

        stream.stream_to_buffer(f)
    return os.path.abspath(stream.default_filename.removesuffix('.mp4'))

def download_audio_raw(url: str, cwd: str) -> str:
    log("Downloading audio...")
    video = pytube.YouTube(url)
    stream = video.streams.filter(only_audio=True).first()
    with open(
        os.path.join(
            cwd,
            stream.default_filename.removesuffix(
                '.mp4'
                )
            ),
        'wb'
        ) as f:

        stream.stream_to_buffer(f)
    return os.path.abspath(stream.default_filename.removesuffix('.mp4'))

def getinfo(video: str):
    return pytube.YouTube(video)

def get_playlist(url: str) -> list:
    yt = pytube.Playlist(url)
    return list(yt.videos)