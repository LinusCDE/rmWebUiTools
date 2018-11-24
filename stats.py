#!/usr/bin/env python3

import api
from collections.abc import Iterable
from statistics import mean, median
from sys import stderr

# ------------------------------
# Config:
DEBUG = False
# ------------------------------


def printStats(files):
    '''
    Collect some interesting stats to show off in console.
    '''
    # Data to collect:
    filesPerFolder = []
    pagesPerNotebook = []
    pagesPerPdf = []
    pagesPerEpub = []


    # Collect data:
    for rmFile in api.iterateAll(files):
        if rmFile.isFolder:
            filesPerFolder.append(len(rmFile.files))
        else:
            pages = rmFile.pages
            if rmFile.isNotebook:
                pagesPerNotebook.append(pages)
            elif rmFile.isPdf:
                pagesPerPdf.append(pages)
            elif rmFile.isEpub:
                pagesPerEpub.append(pages)
            else:
                a = dict()
                raise RuntimeError('Unexpeted filetype for "%s": %s' % (rmFile.path(), rmFile.metadata.get('fileType', '<No fileType-Metadata!>')))

    # Collect root folder / current list as folder if given:
    if isinstance(files, Iterable):
        filesPerFolder.append(len(files))


    # Print collected data:

    # Folders:
    print('Files in folders:')
    folderFormat = '  ' + 4*'{:<14}'
    print(folderFormat.format(
        'TOTAL',
        'MEAN (AVG)',
        'MEDIAN',
        'TOTAL'
    ))
    print(folderFormat.format(
        '%d folders' % len(filesPerFolder),  # "TOTAL"
        '%.1f files' % mean(filesPerFolder),  # "MEAN (AVG)"
        '%.0f files' % median(filesPerFolder), # "MEDIAN"
        '%d files' % sum(filesPerFolder)  # "TOTAL"
    ))

    # Documents/Files:
    print()
    print('Pages in documents:')
    docFormat = '  ' + 6*'{:<14}'
    print(docFormat.format(
        'TYPE',
        'FILES',
        'MEAN (AVG)',
        'MEDIAN',
        'BIGGEST',
        'TOTAL'
    ))
    for typeName, pagesPerType in {'notebook': pagesPerNotebook, 'pdf': pagesPerPdf, 'epub': pagesPerEpub}.items():
        if len(pagesPerType) == 0:
            continue

        print(docFormat.format(
            typeName,  # "TYPE"
            '%d files' % len(pagesPerType),  # "FILES"
            '%.1f pages' % mean(pagesPerType),  # "MEAN (AVG)"
            '%.0f pages' % median(pagesPerType),  # "MEDIAN"
            '%s pages' % max(pagesPerType),  # "BIGGEST"
            '%s pages' % sum(pagesPerType)  # "TOTAL"
        ))

    if len(pagesPerEpub) > 0:
        print('\nThe page statistics of epub may not be correct as the device sometimes has trouble calculating them.')





if __name__ == '__main__':
    try:
        print('Fetching file structure...')
        files = api.fetchFileStructure()
        print()
        printStats(files)
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
