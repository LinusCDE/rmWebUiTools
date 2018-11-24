#!/usr/bin/env python3

import api
from sys import stderr

# ------------------------------
# Config:
DEBUG = False
# ------------------------------

if __name__ == '__main__':
    try:
        print('Fetching file structure...\n', file=stderr)  # Prints to stderr to ignore this if piped into a text file
        files = api.fetchFileStructure()

        print('IDs:')
        for rmFile in api.iterateAll(files):
            print('%s: %s' % (rmFile.id, rmFile.path()))
    except Exception as ex:
        # Error handling:
        if DEBUG:
            raise ex
            exit(1)
        else:
            print('ERROR: %s' % ex, file=stderr)
            print(file=stderr)
            print('Please make sure your reMarkable is connected to this PC and you have enabled the USB Webinterface in "Settings -> Storage".', file=stderr)
            exit(1)
