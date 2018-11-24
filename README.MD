# rmWebUiTools

This is a collection of scripts that utilize the reMarkable USB webinterface to export files.


## Installation

You need to have a recent version of Python 3 as well as these dependencies (to be installed using pip):
- argparse (for export.py)
- requests


## DISCLAIMER

Using the export functionality, the script will prompt your device to **export every single file** onto your pc.
This will - as of now - lead to freezes and other problems, as the software is not specifically suited for this usecase.
I (and probably reMarkable AS) WON'T take any responsibility for potential damage done to your device using this software.

## Usage

The scripts are meant to be ran with python 3 or as executable (on unix systems).

The scripts should run on Windows which currently isn't tested.

Examples:
```
$ python3 export.py --only-notebooks --update NotebookBackup
$ ./export.py --only-notebooks --update NotebookBackup

$ ./tree.py
$ ./paths.py
$ ./countNotebookPages.py
```


## Possibilities

Right now, you can export/mirror all your files into a specified folder, export only changed files or view general information using on of the various scripts available.

You can also make your own scripts using the `api.py` and give you access to all metadata provided by the reMarkable USB webinterface. An example of such information can be found in the file `.exampleRootMetadata.json`.

There is certainly a lot more possible than currently provided.
If you want a certain feature, you can create an issue (= feature request) or contribute it yourself.


## Common problem

When exporting a large amount of files, it can happen that your reMarkable **enters sleep mode** during that process or **locks up and restarts** (happens on some huge pdf files).

When this happens, you can just execute the same command again. It should continue where it failed with no data loss.

