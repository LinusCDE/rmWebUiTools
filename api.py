'''
Utilities regarding the reMarkable usb webinterface.
'''

from collections.abc import Iterable
from datetime import datetime
import requests


RM_WEB_UI_URL = 'http://10.11.99.1'  # No trailing slash!


class RmFile:
    '''
    Representation of a file or folder on the reMarkable device.
    '''

    def __init__(self, metadata, parent=None):
        # Given parameters:
        self.metadata = metadata
        self.parent = parent

        # Hierachial data:
        self.isFolder = (metadata['Type'] == 'CollectionType')
        self.files = [] if self.isFolder else None

        # Determine file type:
        self.isNotebook = not self.isFolder and metadata['fileType'] == 'notebook'
        self.isPdf = not self.isFolder and metadata['fileType'] == 'pdf'
        self.isEpub = not self.isFolder and metadata['fileType'] == 'epub'

        # Easy access of common metadata:
        self.name = metadata['VissibleName'] if 'VissibleName' in metadata else metadata['VisibleName']  # Typo from reMarkable which will probably get fixed in next patch
        self.id = metadata['ID']
        self.isBookmarked = metadata['Bookmarked']
        self.pages = metadata['pageCount'] if not self.isFolder else None
        self.modifiedTimestamp = datetime.strptime(metadata['ModifiedClient'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()


        # Prevent faulty structures:
        if '/' in self.name:
            self.name = self.name.replace('/', '')

    def path(self, basePath=''):
        '''
        Returns the complete path including this file/folder.
        basePath may be provided and prepended.
        '''
        if basePath and not basePath.endswith('/'):
            basePath += '/'

        path = self.name
        parent = self.parent
        while parent:
            path = parent.name + '/' + path
            parent = parent.parent

        return basePath + path

    def parentFolderPath(self, basePath=''):
        '''
        Returns the current folder path that a file is in.
        A basePath may be provided and prepended.

        If in root, the basePath (default '') will be returned.
        '''
        if self.parent:
            if basePath and not basePath.endswith('/'):
                basePath += '/'
            return basePath + self.parent.path()
        else:
            basePath

    def exportPdf(self, targetPath):
        '''
        Downloads this file as pdf to a given path.
        I may take a while before the download is started,
        due to the conversion happening on the reMarkable device.

        Returns bool with True for successful and False for unsuccessful.
        '''
        response = requests.get(RM_WEB_UI_URL + '/download/' + self.id + '/placeholder', stream=True)

        if not response.ok:
            return False

        # Credit: https://stackoverflow.com/a/13137873
        response.raw.decode_content = True  # Decompress if needed

        with open(targetPath, 'wb') as targetFile:
            for chunk in response.iter_content(8192):
                targetFile.write(chunk)
        return True

    def __str__(self):
        return 'RmFile{name=%s}' % self.name

    def __repr__(self):
        return self.__str__()


def iterateAll(filesOrRmFile):
    '''
    Yields all files in this iterable (list, tuple, ...) or file including subfiles and folders.

    In case any (nested) value that isn't a iterable or of class api.RmFile a ValueError will be raised!
    '''
    if isinstance(filesOrRmFile, RmFile):
        # Yield file and optional sub files recursivly:
        yield filesOrRmFile
        if filesOrRmFile.isFolder:
            for recursiveSubFile in iterateAll(filesOrRmFile.files):
                yield recursiveSubFile
    elif isinstance(filesOrRmFile, Iterable):
        # Assumes elements to be of class api.RmFile
        for rmFile in filesOrRmFile:
            for subFile in iterateAll(rmFile):
                yield subFile
    else:
        # Unknown type found!
        raise ValueError('"api.iterateAll(filesOrRmFile)" only accepts (nested) iterables and instances of class api.RmFile !')


def fetchFileStructure(parentRmFile=None):
    '''
    Fetches the fileStructure from the reMarkable USB webinterface.

    Specify a RmFile of type folder to fetch only all folders after the given one.
    Ignore to get all possible file and folders.

    Returns either list of files OR FILLS given parentRmFiles files

    May throw RuntimeError or other releated ones from "requests"
    if there are problems fetching the data from the usb webinterface.
    '''
    if parentRmFile and not parentRmFile.isFolder:
        raise ValueError('"api.fetchFileStructure(parentRmFile)": parentRmFile must be None or of type folder!')

    # Use own list if not parentRmFile is given (aka beeing in root)
    if not parentRmFile:
        rootFiles = []

    # Get metadata:
    directoryMetadataUrl = RM_WEB_UI_URL + '/documents/' + (parentRmFile.id if parentRmFile else '')
    response = requests.get(directoryMetadataUrl)
    response.encoding = 'UTF-8'  # Ensure, all Non-ASCII characters get decoded properly

    if not response.ok:
        raise RuntimeError('Url %s responsed with status code %d' % (directoryMetadataUrl, response.status_code))

    directoryMetadata = response.json()

    # Parse Entries in jsonArray (= files in directory) and request subFolders:
    for fileMetadata in directoryMetadata:
        rmFile = RmFile(fileMetadata, parentRmFile)
        if parentRmFile:
            parentRmFile.files.append(rmFile)
        else:
            rootFiles.append(rmFile)

        # Fetch subdirectories recursivly:
        if rmFile.isFolder:
            fetchFileStructure(rmFile)

    # Return files as list if in root (otherwise the given parentRmFile got their files):
    if not parentRmFile:
        return rootFiles


def findId(filesOrRmFile, fileId):
    '''
    Searched for any file or directory with fileId in given filesOrRmFile (including nested files)

    Returns matching RmFile if found. Otherwise None .
    '''
    for rmFile in iterateAll(filesOrRmFile):
        if rmFile.id == fileId:
            return rmFile
    return None

def getRmFileFor(fileOrFolderPath):
    '''
    Search for given file or folder and return the corresponding RmFile.

    Returns RmFile if file or folder was found. Otherwise None.
    '''
    files = fetchFileStructure()
    for rmFile in iterateAll(files):
        if rmFile.path() == fileOrFolderPath:
            return rmFile
    return None

def changeDirectory(targetFolder):
    '''
    Navigates to a given folder.

    Raises a RuntimeError in case the given targetFolder cannot be found on the device or is not a folder
    '''
    rmFile = getRmFileFor(targetFolder)
    if rmFile is None:
        raise RuntimeError("Folder {} could not be found on device".format(targetFolder))
    if not rmFile.isFolder:
        raise RuntimeError("Given path {} is not a folder on the device".format(targetFolder))
    
    requests.post(RM_WEB_UI_URL + "/documents/" + rmFile.id)

def upload(file):
    '''
    Uploads a file given by the provided file handle to the currently selected folder.
    '''
    files = {'file': file}
    response = requests.post(RM_WEB_UI_URL + "/upload", files=files)
    if not response.ok:
        raise RuntimeError('Upload failed with status code %d' % (response.status_code))
