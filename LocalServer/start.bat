@echo off
setlocal enabledelayedexpansion

REM === 1. 프로젝트 루트 경로 설정 ===
set "ROOT_DIR=%~dp0"
set "NGROK_SRC=C:\ProgramData\chocolatey\bin\ngrok.exe"
set "NGROK_DST=%ROOT_DIR%ngrok.exe"

REM === 2. ngrok.exe가 프로젝트 루트에 없다면 복사 또는 choco로 설치 (관리자 권한 필요)
if not exist "%NGROK_DST%" (
    if exist "%NGROK_SRC%" (
        echo [ngrok.exe를 시스템에서 프로젝트 루트로 복사 중...]
        copy /Y "%NGROK_SRC%" "%NGROK_DST%"
        if exist "%NGROK_DST%" (
            echo [복사 성공! %NGROK_DST%]
        ) else (
            echo [복사 실패! 권한 문제 등 확인 필요.]
        )
    ) else (
        echo [시스템 ngrok.exe가 존재하지 않습니다. choco로 설치를 먼저 시도합니다.]
        choco install ngrok -y
        if exist "%NGROK_SRC%" (
            echo [설치된 ngrok.exe를 복사합니다.]
            copy /Y "%NGROK_SRC%" "%NGROK_DST%"
            if exist "%NGROK_DST%" (
                echo [복사 성공! %NGROK_DST%]
            ) else (
                echo [설치 후 복사도 실패! 권한 문제 등 확인 필요.]
            )
        ) else (
            echo [ngrok.exe 설치 및 복사 실패. 수동 확인 필요.]
        )
    )
) else (
    echo [프로젝트 루트에 이미 ngrok.exe가 존재합니다.]
)

REM === (필요시) 가상환경 활성화 ===
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

REM === 7. 서버 실행
start "" cmd /k "python -m app.main"
echo [완료] 서버를 시작했습니다.

REM === 6. ngrok이 완전히 뜨길 기다림(10초 대기, 필요시 늘릴 수 있음)
timeout /t 10 >nul

REM === 5. ngrok 실행 (순서 변경)
start "" cmd /k "python app\ngrok_Start.py"
echo [완료] ngrok이 실행되었습니다.

REM === 8. (참고) 배치 파일 자동 종료(스케줄러 등록용) ===
REM pause

REM === 9. 배치 종료 ===
exit
