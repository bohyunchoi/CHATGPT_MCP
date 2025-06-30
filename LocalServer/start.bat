@echo off
setlocal enabledelayedexpansion

REM === 1. 프로젝트 루트 경로 설정 ===
set ROOT_DIR=%~dp0

REM === 2. (필요시) 가상환경 활성화 ===
REM call "%ROOT_DIR%\.venv\Scripts\activate"

REM === DB 접속 정보 설정 ===
IF NOT DEFINED MSSQL_SERVER set "MSSQL_SERVER=10.31.20.6"
IF NOT DEFINED MSSQL_USER set "MSSQL_USER=sa"
IF NOT DEFINED MSSQL_PASSWORD set "MSSQL_PASSWORD=f$ei#L!sa"
IF NOT DEFINED MSSQL_DATABASE set "MSSQL_DATABASE=master"

REM === 3. 프로젝트 루트로 이동 ===
cd /d "%ROOT_DIR%"

REM === 4. 기존 프로세스 종료(선택사항, 이미 실행중일 경우 강제종료) ===
REM taskkill /im python.exe /f >nul 2>&1
REM taskkill /im uvicorn.exe /f >nul 2>&1

REM === 5. ngrok 실행 (순서 변경)
start "" cmd /k "python app\ngrok_Start.py"

echo [완료] ngrok이 실행되었습니다.

REM === 6. ngrok이 완전히 뜨길 기다림(10초 대기, 필요시 늘릴 수 있음)
timeout /t 10 >nul

REM === 7. 서버 실행
start "" cmd /k "python -m app.main"
REM 또는 uvicorn 직접 실행시 (아래 주석 해제)
REM start "" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [완료] 서버를 시작했습니다.

REM === 8. (참고) 배치 파일 자동 종료(스케줄러 등록용) ===
REM 필요시 아래 pause를 제거하고 자동 종료
REM pause

REM === 9. 배치 종료 ===
exit
