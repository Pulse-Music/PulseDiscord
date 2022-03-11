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

# This is a module that should be imported before running the main program.
# DO NOT RUN THIS MODULE DIRECTLY.

assert __name__ != "__main__", "This module should not be run directly. Import it instead."
def resolve_conflicts(FS_NAME: str="FileStorage", CONFIG_YML: str ="config.yml") -> None:
    import os, shutil, yaml
    if os.path.isdir(CONFIG_YML):
        shutil.rmtree(CONFIG_YML, ignore_errors=True)
    
    if os.path.isfile(CONFIG_YML):
        with open(CONFIG_YML, 'r') as f:
            config = yaml.safe_load(f)
        if config is None:
            config = {
                "token": None,
                "prefix": ".",
                "profile_picture": None,
                "name": None,
                "status": 'online',
                "activity": {"type": 'listening', "name": 'Your commands'},
                }
            with open(CONFIG_YML, 'w') as f:
                yaml.dump(config, f)

    
    # Ready the File System for archiving.
    if os.path.isfile(FS_NAME):
        os.remove(FS_NAME)
        os.makedirs(FS_NAME, exist_ok=False)

    if not os.path.isdir(FS_NAME):
        os.makedirs(FS_NAME, exist_ok=False)

    