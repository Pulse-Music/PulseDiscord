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


# This is the logger module. (Not in pypi)
assert __name__ != "__main__", "This module should not be run directly. Import it instead."
import datetime
import os
from termcolor import colored
import colorama

class Logger:
    def __init__(self):
        colorama.init()
        date = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
        self.log_file_name = "logs/" + date
        if os.path.isfile("logs"):
            try:
                os.remove("logs")
                os.mkdir("logs")
            except [OSError, PermissionError]:
                print("[ERROR] Unable to create logs directory")
        elif os.path.isdir("logs"):
            pass
        else:
            os.mkdir("logs")
        self.log_file = open(self.log_file_name, "a")
        self.setup()

    # Override
    def setup():
        pass

    def log2(self, message, type_):
        pass

    def log(self, message, type_):
        # Get the current time with milliseconds
        # time = datetime.datetime.now().strftime('%H:%M:%S:%f')
        time = datetime.datetime.now().strftime("%H:%M:%S")
        # format_ = f'[{time}]-[{type_.upper()}]: {message}'
        types = {"info": "green", "warning": "yellow", "error": "red", "debug": "cyan"}
        format_ = f'[{colored(time, "yellow")}]-\
[{colored(type_.upper(), types[type_])}]: \
{colored(message, "white")}'
        file_format = f"[{time}]-[{type_.upper()}]: {message}\n"
        try:
            print(format_)
        except AttributeError:
            pass
        try:
            self.log_file.write(file_format)
        except UnicodeEncodeError:
            for char in file_format:
                try:
                    self.log_file.write(char)
                except UnicodeEncodeError:
                    pass

        del format_, file_format
        self.log2(message, type_)
        return f"[{time}]-[{type_.upper()}]: {message}"

    def quit(self):
        self.log_file.close()
        colorama.deinit()
