@echo off
setlocal

:: hide any "UNC paths are not supported" warnings
cls

:: If this batch file is on a UNC path, then its folder will be mapped to new a drive letter
:: (that will be removed later by the popd command).
:: pushd will change your working directory to the scripts location in the new mapped drive.
@pushd %~dp0

set VENV=venv
set DEST=_backup

if not exist %VENV% (
    echo ===== CREATING VIRTUAL ENVIROMENT
    py -3 -m venv %VENV%
    echo ===== ACTIVATE VIRTUAL ENVIROMENT
    call %VENV%\scripts\activate.bat
    echo ===== UPGRADING PIP
    python -m pip install --upgrade pip
    echo ===== INSTALLING REQUIREMENTS
    pip install --requirement requirements.txt
) else (
    echo ===== ACTIVATE VIRTUAL ENVIROMENT
    call %VENV%\scripts\activate.bat
)

if not exist %DEST% mkdir %DEST%
echo ===== EXPORTING FROM REMARKABLE
python export.py --update %DEST%

:: popd to clean up the mapped drive, if created.
@popd

pause
