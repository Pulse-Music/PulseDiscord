import subprocess
def mpv(url):
    subprocess.Popen("start /b " + "mpv\\mpv.exe " + url + "--no-video", shell=True)