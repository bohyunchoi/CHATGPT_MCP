@echo off
setlocal enabledelayedexpansion

:: Assume this script lives in the LocalServer folder
set ROOT_DIR=%~dp0

cd /d "%ROOT_DIR%"

:: DB connection settings
IF NOT DEFINED MSSQL_SERVER set "MSSQL_SERVER=10.31.20.6"
IF NOT DEFINED MSSQL_USER set "MSSQL_USER=sa"
IF NOT DEFINED MSSQL_PASSWORD set "MSSQL_PASSWORD=f$ei#L!sa"
IF NOT DEFINED MSSQL_DATABASE set "MSSQL_DATABASE=master"

:: Start ngrok first
echo [INFO] Starting ngrok...
start "ngrok" "%ROOT_DIR%ngrok.exe" http 8000 > "%ROOT_DIR%ngrok.log" 2>&1

:: Wait for ngrok tunnel (up to 30 seconds)
set /a NGROK_WAIT=0
:WAIT_NGROK
set /a NGROK_WAIT+=1
for /f "delims=" %%A in ('powershell -Command "(Invoke-RestMethod -ErrorAction SilentlyContinue -Uri http://127.0.0.1:4040/api/tunnels).tunnels[0].public_url"') do set NGROK_URL=%%A
if not defined NGROK_URL (
    if %NGROK_WAIT% GEQ 30 (
        echo [WARN] ngrok tunnel not detected. Continuing...
    ) else (
        timeout /t 1 >nul
        goto WAIT_NGROK
    )
)

:: Launch the application after ngrok is ready
echo [INFO] Launching application...
start "app" cmd /k "python -m app.main"

echo [INFO] All processes started.
pause
