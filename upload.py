#!/usr/bin/env python3
'''
Upload - Upload either PDFs or ePubs to your remarkable.
'''


import api
import argparse

from sys import stderr

# ------------------------------
# Config:
DEBUG = False
# ------------------------------

def uploadTo(files, targetFolder):
    api.navigateTo(targetFolder)
    for file in files:
        try:
           api.upload(file)
        except Exception as ex:
            print('ERROR: Failed to upload "%s" to "%s"' % (file, targetFolder))
            raise ex
        finally:
            file.close()

def printUsageAndExit():
    print('Usage: %s <Target-Folder>' % argv[0], file=stderr)
    exit(1)


if __name__ == '__main__':
    # Argument parsing:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    ap.add_argument('-t', '--target-folder', help='Folder on your remarkable to put the uploaded files in')
    ap.add_argument('file', type=argparse.FileType('rb'), nargs='+')

    args = ap.parse_args()

    try:
        uploadTo(args.file, args.target_folder)
        print('Done!')
    except KeyboardInterrupt:
        print('Cancelled.')
        exit(0)
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
