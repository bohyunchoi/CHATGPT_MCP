@echo off
setlocal enabledelayedexpansion

:: ��ũ��Ʈ ��ġ�� ������Ʈ ��Ʈ(��\LocalServer)��� ����
set ROOT_DIR=%~dp0

:: (����) ����ȯ�� Ȱ��ȭ, ����ȯ���� �ִٸ�
:: call "%ROOT_DIR%\.venv\Scripts\activate"

:: ������Ʈ ��Ʈ�� �̵�
cd /d "%ROOT_DIR%"

:: Python -m ���� ��Ű�� ���� (app.main ����)
start "" cmd /k "python -m app.main"

:: �Ǵ� Uvicorn ���� ����
:: start "" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [�Ϸ�] ������ �����߽��ϴ�.
pause
