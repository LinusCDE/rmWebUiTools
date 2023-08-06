#!/usr/bin/env python3
'''
Upload - Upload either PDFs or ePubs to your remarkable.
'''


import api
import argparse
import os

from sys import stderr

def printUsageAndExit():
    print('Usage: %s <Target-Folder>' % argv[0], file=stderr)
    exit(1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    ap.add_argument('-t', '--target-folder', help='Folder on your remarkable to put the uploaded files in')
    ap.add_argument('file', type=argparse.FileType('rb'), nargs='+')

    args = ap.parse_args()

    try:
        api.changeDirectory(args.target_folder)
        for file in args.file:
            file_name, file_extension = os.path.splitext(file.name)
            if file_extension.lower() not in [".pdf", ".epub"]:
                print('Only PDFs and ePubs are supported. Skipping {}'.format(file.name))    
                continue
            print('Uploading {} to {}'.format(file.name, args.target_folder))
            api.upload(file)
            print('Successfully uploaded {} to {}'.format(file.name, args.target_folder))
        print('Done!')
    except KeyboardInterrupt:
        print('Cancelled.')
        exit(0)
    except Exception as ex:
        print('ERROR: %s' % ex, file=stderr)
        print(file=stderr)
        print('Please make sure your reMarkable is connected to this PC and you have enabled the USB Webinterface in "Settings -> Storage".', file=stderr)
        exit(1)
    finally:
        for file in args.file:
            file.close()
