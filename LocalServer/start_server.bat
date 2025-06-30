@echo off
setlocal enabledelayedexpansion

:: 스크립트 위치가 프로젝트 루트(…\LocalServer)라고 가정
set ROOT_DIR=%~dp0

:: (선택) 가상환경 활성화, 가상환경이 있다면
:: call "%ROOT_DIR%\.venv\Scripts\activate"

:: 프로젝트 루트로 이동
cd /d "%ROOT_DIR%"

:: Python -m 으로 패키지 실행 (app.main 으로)
start "" cmd /k "python -m app.main"

:: 또는 Uvicorn 직접 실행
:: start "" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [완료] 서버를 시작했습니다.
pause
