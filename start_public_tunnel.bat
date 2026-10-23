@echo off
echo ===================================================
echo   FlagFall CTFd - Free Instant Public Tunnel
echo ===================================================
echo.
echo Launching public HTTPS tunnel...
cloudflared.exe tunnel --protocol http2 --url http://127.0.0.1:8000
pause
