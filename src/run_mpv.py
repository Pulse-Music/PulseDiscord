import subprocess
def mpv(url):
    subprocess.Popen("start /b " + "mpv\\mpv.exe " + url + "--no-video", shell=True)

mpv('https://www.youtube.com/watch?v=BS-81QMqqd8')