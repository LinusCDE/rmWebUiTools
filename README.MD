# rmWebUiTools

[![Mentioned in Awesome reMarkable](https://awesome.re/mentioned-badge.svg)](https://github.com/reHackable/awesome-reMarkable)

This is a collection of scripts that utilize the reMarkable USB web interface to export files.


## DISCLAIMER

Using the export functionality, the script will prompt your device to **export every single file** onto your pc.
This will - as of now - lead to freezes and other problems, as the software is not specifically suited for this use case.

I (and reMarkable AS too) **WON'T take any responsibility** for potential damage done to your device using this software.


## Installation

First ensure you have a recent version of [Python 3](https://www.python.org/downloads/) installed.

To install all dependencies, execute this command in your terminal or command prompt:
```
$ pip install requests
```

Next you clone this repository (or download it as a zip file), and go into the folder using the `cd` command in your terminal or command prompt.


## Usage

The scripts (except `api.py`) are meant to be executed with python 3.

This can be done by typing `python` followed by the name of the script file.
On unix systems, you can also execute those scripts like any other shell script.

Examples:
```
$ python export.py --only-notebooks --update NotebookBackup
$ ./export.py --only-notebooks --update NotebookBackup
$ ./export.py --help

$ ./tree.py
$ ./paths.py
$ ./stats.py
```


## Possibilities

Right now, you can export/mirror all your files into a specified folder, export only changed files or view general information using on of the various scripts available.

You can also make your own scripts using the `api.py` and give you access to all metadata provided by the reMarkable USB web interface. An example of such information can be found in the file `.exampleRootMetadata.json`.

There is certainly a lot more possible than currently provided.
If you want a certain feature, you can create an issue (= feature request) or contribute it yourself.


## Common problem

When exporting a large amount of files, it can happen that your reMarkable **enters sleep mode** during that process or **locks up and restarts** (happens on some huge pdf files).

When this happens, you can just execute the same command again. It should continue where it failed with no data loss.
