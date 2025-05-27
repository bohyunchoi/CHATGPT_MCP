@echo off
cd /d %~dp0

REM 토큰이 포함된 GitHubPush.bat 완전히 삭제
del GitHubPush.bat

REM 기존 커밋 히스토리 전부 제거하고 새로 시작
rd /s /q .git
git init
git remote add origin git@github.com:bohyunchoi/CHATGPT_MCP.git
git checkout -b main

REM 사용자 정보 설정
git config user.name "bohyunchoi"
git config user.email "bohyun43@naver.com"

REM 전체 파일 다시 커밋 후 강제 푸시
git add .
git commit -m "민감 정보 제거 후 초기화"
git push -f origin main

echo ✅ Git 커밋 히스토리를 초기화하고 푸시했습니다.