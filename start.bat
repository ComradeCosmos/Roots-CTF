@echo off
echo ===================================================
echo   RootsCTF / Civilization - CTFd Server Launcher
echo ===================================================
echo.
echo Navigating to CTFd directory...
cd CTFd
if exist ..\.venv\Scripts\python.exe (
    echo Launching with root virtualenv...
    ..\.venv\Scripts\python.exe serve.py --port 8000
) else if exist .venv\Scripts\python.exe (
    echo Launching with CTFd virtualenv...
    .venv\Scripts\python.exe serve.py --port 8000
) else (
    echo Launching with Python...
    python serve.py --port 8000
)
pause
