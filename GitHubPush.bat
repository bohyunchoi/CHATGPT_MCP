@echo off
cd /d %~dp0

REM GitHub 자격 증명 삭제
git credential-manager erase https://github.com

REM 원격 주소를 HTTPS로 재설정
git remote set-url origin https://github.com/bohyunchoi/CHATGPT_MCP.git

REM 인코딩 설정
chcp 65001 >nul

git add .
git commit -m "hello.py 업로드"
git push origin main

echo ✅ hello.py가 GitHub에 업로드되었습니다.