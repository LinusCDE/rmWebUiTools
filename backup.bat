@echo off
setlocal

set VENV=venv
set DEST=_backup

if not exist %VENV% (
    py -3 -m venv %VENV%
    call %VENV%\scripts\activate
    python -m pip install --upgrade pip
    pip install --requirement requirements.txt
) else (
    call %VENV%\scripts\activate
)

if not exist %DEST% mkdir %DEST%
export.py --update %DEST%

pause
