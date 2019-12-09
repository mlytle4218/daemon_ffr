# Daemon model for recording streams
Interface to start, stop and modify recording of audio and video streams through ffmpeg primarily and secondarily in Docker containers.

## Based on work from The Socket Programming in Python
[Socket Programming in Python (Guide)](https://realpython.com/python-sockets/).

## Requirements

- [Python](https://www.python.org/) 3.6 or later.


notes:
[killing ffmpeg](https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true)  
signal.SIGTERM stops process  
signal.SIGSTOP pauses process  
signal.SIGCONT restarts process  