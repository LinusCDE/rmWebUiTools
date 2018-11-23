#!/usr/bin/env python3

from os import makedirs
from os.path import exists
import requests
import shutil
from sys import argv, stderr

RM_WEB_UI_URL = 'http://10.11.99.1'  # No trailing slash!


class RmFile:
    def __init__(self, metadata, parent=None):
        self.metadata = metadata
        self.parent = parent

        self.isFolder = (metadata['Type'] == 'CollectionType')
        self.children = [] if self.isFolder else None

        self.name = metadata[
            'VissibleName'] if 'VissibleName' in metadata else metadata['VisibleName']  # Typo from reMarkable which will probably get fixed in next patch
        self.id = metadata['ID']
        self.isBookmarked = metadata['Bookmarked']

        # Prevent faulty structures:
        if '/' in self.name:
            name = name.replace('/', '')
    
    def getPath(self, basePath=''):
        if basePath and not basePath.endswith('/'):
            basePath += '/'
        
        path = self.name
        parent = self.parent
        while parent:
            path = parent.name + '/' + path
            parent = parent.parent
        
        return basePath + path

    def getParentDirectory(self, basePath=''):
        if self.parent:
            if basePath and not basePath.endswith('/'):
                basePath += '/'
            return basePath + self.parent.getPath()
        else:
            basePath

    def download(self, targetFilePath):
        '''
        Returns bool with True for successful and False for unsuccessful
        '''
        response = requests.get(RM_WEB_UI_URL + '/download/' + self.id + '/placeholder', stream=True)

        if not response.ok:
            return False

        # Credit: https://stackoverflow.com/a/13137873
        response.raw.decode_content = True  # Decompress if needed

        with open(targetFilePath, 'wb') as targetFile:
            for chunk in response.iter_content(8192):
                targetFile.write(chunk)
        return True

    def iterRecursive(self):
        if not self.isFolder:
            return
        
        for child in self.children:
            yield child
            for recursiveChild in child.iterRecursive():
                yield recursiveChild

    def __str__(self):
        return 'RmFile{name=%s}' % self.name

    def __repr__(self):
        return self.__str__()


def iterAllFiles(files):
    for rmFile in files:
        yield rmFile
        for child in rmFile.iterRecursive():
            yield child


def downloadAllTo(files, targetFolderPath):
    downloadableFiles = list(filter(lambda rmFile: rmFile.isFolder is False, iterAllFiles(files)))
    totalDownloadableFiles = len(downloadableFiles)

    lastDirectory = None
    for i, downloadableFile in enumerate(downloadableFiles):

        # Announce directory change:
        directory = downloadableFile.getParentDirectory()
        if(directory != lastDirectory):
            print('INFO: Aktuelles Verzeichnis: %s' % directory)
            lastDirectory = directory
        
        # Get full path:
        path = downloadableFile.getPath(targetFolderPath)
        if not path.endswith('.pdf'):
            path += '.pdf'

        # Create necessary directories:
        parentDir = downloadableFile.getParentDirectory(targetFolderPath)
        if parentDir:  # May be None in the root
            makedirs(parentDir, exist_ok=True)

        # Download is file not existing:
        if(exists(path)):
            print('INFO: [%d/%d] Überspringe Datei \'%s\' (existiert bereits im Ziel-Verzeichnis)...' % (i+1, totalDownloadableFiles, downloadableFile.name))
        else:
            print('INFO: [%d/%d] Erstelle und lade PDF-Datei von \'%s\' herunter...' % (i+1, totalDownloadableFiles, downloadableFile.name))
            downloadableFile.download(path)
        


def findById(files, searchedId):
    for currentFile in files:
        if currentFile.id == searchedId:
            return currentFile
        possibleMatch = findById(currentFile.children, searchedId) if currentFile.isFolder else None
        if possibleMatch:
            return possibleMatch
    return None  # Also the default behaviour of python


def fetchFileStructure() -> list:
    fetchedFiles = []  # List of RmFile classes in root

    nonFetchedFolderIds = [
    ]  # All RmFiles which are folders and not yet fetched
    fetchRoot = True  # Fetch root instead of entries in "nonFetchedFolderIds"

    while fetchRoot or len(nonFetchedFolderIds) > 0:
        # Error checking:
        if (fetchRoot and len(nonFetchedFolderIds) > 0):
            print(
                'ERROR: Can\'t have task to fetch Root while having other unfetched folders!',
                file=stderr)
            exit(1)

        # Take current folder as url:
        if fetchRoot:
            currentUrl = RM_WEB_UI_URL + '/documents/'  # The trailing slash is important for the server!
        else:
            currentUrl = RM_WEB_UI_URL + '/documents/' + nonFetchedFolderIds.pop(
                0)

        # Get metadata:
        response = requests.get(currentUrl)
        response.encoding = 'UTF-8'  # Ensure, all Non-ASCII characters get decoded properly

        if not response.ok:
            print(
                'ERROR: Get status code %d for url \'%s\'' %
                (response.status_code, currentUrl),
                file=stderr)
            exit(1)

        entries = response.json()
        for entry in entries:
            parentId = entry['Parent']
            folder = findById(fetchedFiles, parentId)

            if not folder and not fetchRoot:
                print(
                    'ERROR: Parent (Id: %s) not yet fetched or non-existant!' %
                    parentId,
                    file=stderr)
                exit(1)

            rmFile = RmFile(entry, folder)
            if folder:
                folder.children.append(rmFile)

            # Add to structure:
            if rmFile.isFolder:
                nonFetchedFolderIds.append(rmFile.id)
            if fetchRoot:
                fetchedFiles.append(rmFile)

        if fetchRoot:
            fetchRoot = False

    return fetchedFiles


if __name__ == '__main__':
    if len(argv) != 2:
        print('Aufruf: %s <Ziel-Ordner>' % argv[0], file=stderr)
        print('WARNUNG: Bestehende Datein werden nicht überschrieben!')
        exit(1)
    
    targetFolder = argv[1]
    print('INFO: Erstelle index aller Dateien...')

    try:
        files = fetchFileStructure()
    except:
        files = None

    if not files:
        print('ERROR: Fehler beim Auflisten der Datein!', file=stderr)
        print('ERROR: Bitte stelle sicher, dass das reMarkable angeschlossen ist', file=stderr)
        print('       und die Weboberfläche aktiv ist.', file=stderr)
        exit(1)

    print('Konvertiere und downloade alle Datein in den Ordner \'%s\'' % targetFolder)
    downloadAllTo(files, targetFolder)
    print('Fertig')
