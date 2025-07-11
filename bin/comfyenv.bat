@echo off
setlocal

REM Check if CONDA_ROOT is already set
if defined CONDA_ROOT (
    goto :run
)

REM echo CONDA_ROOT not set. Attempting to detect Conda...

REM Try to find conda in PATH
for %%I in (conda) do (
    if not "%%~$PATH:I"=="" (
        set "FOUND_CONDA=%%~$PATH:I"
    )
)

if defined FOUND_CONDA (
    REM Strip bin\conda.exe to get CONDA_ROOT
    for %%F in ("%FOUND_CONDA%") do (
        set "CONDA_ROOT=%%~dpF"
        REM Remove trailing \Scripts or \bin
        for %%D in ("%CONDA_ROOT%..\") do set "CONDA_ROOT=%%~fD"
    )
    REM echo Detected CONDA_ROOT: %CONDA_ROOT%
    goto :run
)

REM Try common paths
set "POSSIBLE_PATHS=%USERPROFILE%\miniconda3;%USERPROFILE%\anaconda3;C:\ProgramData\miniconda3;C:\Miniconda3"

for %%P in (%POSSIBLE_PATHS%) do (
    if exist "%%P\condabin\conda.bat" (
        set "CONDA_ROOT=%%P"
        REM echo Found CONDA_ROOT at fallback path: %CONDA_ROOT%
        goto :run
    )
)

:run
    set BIN_DIR=%~dp0
    set PATH=%BIN_DIR%;%CONDA_ROOT%/condabin;%PATH%
    %CONDA_ROOT%/python.exe %BIN_DIR%/../main.py %*
    exit /b %ERRORLEVEL%

echo Error: Conda not found. Please install Conda or set CONDA_ROOT manually.
exit /b 1
