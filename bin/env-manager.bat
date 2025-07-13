@echo off
setlocal

set BIN_DIR=%~dp0
set PATH=%BIN_DIR%;%PATH%
REM Check if CONDA_ROOT is already set
call _conda_root.bat

%CONDA_ROOT%/python.exe %BIN_DIR%/../env_manager_main.py %*
exit /b %ERRORLEVEL%
