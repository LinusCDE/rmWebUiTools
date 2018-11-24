#!/usr/bin/env python3

import api
from sys import stderr

# ------------------------------
# Config:
DEBUG = False
# ------------------------------


if __name__ == '__main__':
    try:
        print('Fetching file structure...')
        files = api.fetchFileStructure()

        totalPages = 0
        for rmFile in api.iterateAll(files):
            if rmFile.isNotebook:
                totalPages += rmFile.pages
        
        print('All your notebooks have a combined amount of %d pages.' % totalPages)
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
