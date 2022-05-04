from pytube import YouTube

class YouTube(YouTube):

    @property
    def thumbnail(self):
        return f"https://img.youtube.com/vi/{self.video_id}/maxresdefault.jpg"