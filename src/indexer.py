import pytube
import os
from threading import Thread

def search(query):
    print("Searching for " + query + "...")
    yt = pytube.Search(query)
    return yt.results

def download_audio(video: pytube, cwd: str):
    print("Downloading audio...")
    stream: pytube.Stream = video.streams.filter(only_audio=True).first()
    print(stream.default_filename)
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
    return stream.default_filename.removesuffix('.mp4')

