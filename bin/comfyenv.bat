@echo off
set BIN_DIR=%~dp0
set PATH=%BIN_DIR%;%PATH%
%CONDA_ROOT%/python.exe %BIN_DIR%/../main.py %*