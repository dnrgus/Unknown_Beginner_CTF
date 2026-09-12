@echo off
setlocal
title UNKNOWN Beginner CTF Launcher
chcp 65001 >nul

set "SCRIPT_DIR=%~dp0"
set "PS1=%SCRIPT_DIR%Launch-UNKNOWN-Beginner-CTF.ps1"

if not exist "%PS1%" (
  echo Launch-UNKNOWN-Beginner-CTF.ps1 file was not found.
  echo.
  pause
  exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
exit /b %ERRORLEVEL%
