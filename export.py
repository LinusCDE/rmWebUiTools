#!/usr/bin/env python3
'''
Export - Exports all files of the remarkable onto your PC as pdfs.

Info: If a file is already exported, it will get skipped by default.
'''


import api

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from os import makedirs, utime
from os.path import exists, getmtime
from sys import stderr

# ------------------------------
# Config:
DEBUG = False
# ------------------------------

def exportTo(files, targetFolderPath, onlyNotebooks, updateFiles):
    exportableFiles = list(filter(lambda rmFile: rmFile.isFolder is False, api.iterateAll(files)))

    # Filter for only notebooks if requested:
    if onlyNotebooks:
        exportableFiles = list(filter(lambda rmFile: rmFile.isNotebook, exportableFiles))

    totalExportableFiles = len(exportableFiles)

    lastDirectory = None
    for i, exportableFile in enumerate(exportableFiles):

        # Announce directory change:
        directory = exportableFile.parentFolderPath()
        if(directory != lastDirectory):
            print('INFO: Current folder: %s' % ('<reMarkable Document Root>' if not directory else directory))
            lastDirectory = directory

        # Get full path:
        path = exportableFile.path(targetFolderPath)
        if not path.endswith('.pdf'):
            path += '.pdf'

        # Create necessary directories:
        parentDir = exportableFile.parentFolderPath(targetFolderPath)
        if parentDir:  # May be None in the root
            makedirs(parentDir, exist_ok=True)

        # Check if file needs to be downloaded and output appropriate messages:
        skipFile = False
        if exists(path):
            # Existing exported file:
            if updateFiles:
                if int(getmtime(path)) < int(exportableFile.modifiedTimestamp):
                    # Update outdated export:
                    print('INFO: [%d/%d] Updating file \'%s\'...' % (i+1, totalExportableFiles, exportableFile.name))
                else:
                    # Skip file that is up-to-date:
                    skipFile = True
                    print('WARN: [%d/%d] Skipping unchanged file \'%s\'...' % (i+1, totalExportableFiles, exportableFile.name))
            else:
                # Don't override files. Regardless of date:
                skipFile = True
                print('INFO: [%d/%d] Skipping file \'%s\' (already exists in your target folder)...' % (i+1, totalExportableFiles, exportableFile.name))
        
        if not exists(path):
            # File never exported:
            print('INFO: [%d/%d] Exporting \'%s\'...' % (i+1, totalExportableFiles, exportableFile.name))
        
        # Export file if necessary:
        if not skipFile:
            exportableFile.exportPdf(path)
            utime(path, (exportableFile.modifiedTimestamp, exportableFile.modifiedTimestamp))  # Use timestamp from the reMarkable device


def printUsageAndExit():
    print('Usage: %s [--only-notebooks] [--override-modified] <Target-Folder>' % argv[0], file=stderr)
    print('WARNING: Existing files won''t get overridden (helpful for continuing an interrupted export).')
    exit(1)


if __name__ == '__main__':

    # Argument parsing:
    ap = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter)

    ap.add_argument('target_folder', help='Base folder to put the exported files in')

    ap.add_argument(
        '-n', '--only-notebooks',
        action='store_true', default=False, help='Skips all files except notebooks')

    ap.add_argument(
        '-u', '--update',
        action='store_true', default=False, help='Overrides/Updates all updated files. Does not remove deleted files!')

    args = ap.parse_args()
    targetFolder, onlyNotebooks, updateFiles = args.target_folder, args.only_notebooks, args.update


    # Print info regarding arguments:
    if updateFiles:
        print('INFO: Updating files that have been changed recently. (Does not delete old files.)')
    if onlyNotebooks:
        print('INFO: Export only notebooks.')


    try:
        # Actual process:
        print('INFO: Fetching file structure...')
        files = api.fetchFileStructure()
        exportTo(files, targetFolder, onlyNotebooks, updateFiles)
        print('Done!')
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

    
