@echo off
setlocal

set "TOOLS_DIR=%~dp0"
for %%I in ("%TOOLS_DIR%\..\..") do set "REPO_ROOT=%%~fI"
set "VENV_DIR=%REPO_ROOT%\.ai\runtime\venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "ENGINE=%TOOLS_DIR%agent_rails_memory.py"

if not exist "%VENV_PY%" (
  python -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)" >nul 2>nul
  if not errorlevel 1 (
    python -m venv "%VENV_DIR%"
  ) else (
    py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)" >nul 2>nul
    if not errorlevel 1 py -3 -m venv "%VENV_DIR%"
  )
)

if not exist "%VENV_PY%" (
  echo {"ok":false,"error":"Python 3.11 or newer was not found, or .ai/runtime/venv could not be created. Install Python with venv support and verify the repository is writable."}
  exit /b 3
)

"%VENV_PY%" -c "import sqlite3; c=sqlite3.connect(':memory:'); c.execute('CREATE VIRTUAL TABLE t USING fts5(x)')" >nul 2>nul
if errorlevel 1 (
  echo {"ok":false,"error":"The selected Python sqlite3 module does not include FTS5. Install a Python 3.11+ build with FTS5."}
  exit /b 3
)

"%VENV_PY%" "%ENGINE%" %*
exit /b %errorlevel%
