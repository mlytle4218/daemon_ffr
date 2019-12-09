#!/usr/bin/env python3
import datetime, time
import config

def log(input):
    with open(config.LOG_FILE, "a") as myfile:
        string = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')
        string = string + ' - ' + str(input) + '\n'
        myfile.write(string)