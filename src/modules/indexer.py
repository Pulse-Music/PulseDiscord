# MIT License
#
# Copyright (c) 2022-Present Advik-B <advik.b@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# assert __name__ != "__main__", "This module should not be run directly. Import it instead."
import pytube
import py7zr
import requests
import asyncio
import os

CACHE_PATH = 'cache' 

def before_start():
    """ Before the bot starts """
    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)


async def search(query:str, max_results:int=None):
    """ Search for a video on YouTube """
    if max_results is None:
        max_results = 10
    return pytube.YouTube(query).search(max_results=max_results)

async def download_audio(video:pytube.YouTube):
    """ Download the audio of a video """
    audio = video.streams.filter(only_audio=True).first()
    path = os.path.join(CACHE_PATH, video.video_id + '.mp3')
    with open(path, 'wb') as f:
        audio.stream_to_buffer(f)
    return path

def cache_video(path:str):
    """ Cache a video and zip it """

    with py7zr.SevenZipFile(path, 'wb') as archive:
        archive.write(file=path)

def main():
    before_start()
    """ Main function """
    video = pytube.YouTube('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    asyncio.run(download_audio(video))

if __name__ == "__main__":
    main()
