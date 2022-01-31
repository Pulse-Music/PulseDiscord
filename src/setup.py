import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "packages": [
        'pyyaml'
        'discord'
        'pytube'
        'discord[voice]'
        'discord[audio]'
        'termcolor'
        'discord',
        
        ],
    "excludes": [
        
        'tkinter',
    ],
    'include_files':['ffmpeg/', ],
    "include_msvcr": True,
    
}

base = "win32"

setup(
    name = "YouTube Discord Bot",
    version = "1",
    description = "A bot that plays YouTube audio in Discord",
    options = {"build_exe": build_exe_options,},
    executables = [
        Executable(
            "bot.py",
            base=base,
            icon='assets/icon.ico'
            )
        ]
    )
