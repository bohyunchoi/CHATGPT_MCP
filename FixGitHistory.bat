@echo off
cd /d %~dp0

REM GitHubPush.bat 파일에서 민감 정보 제거 (SSH 방식으로 변경)
powershell -Command "(Get-Content GitHubPush.bat) -replace 'https://ghp_.*@github.com', 'git@github.com' | Set-Content GitHubPush.bat"

REM 최근 커밋 되돌리기
git reset --soft HEAD~1

REM 변경된 GitHubPush.bat 스테이징 해제 및 복원
git restore --staged GitHubPush.bat
git restore GitHubPush.bat

REM 수정 후 재커밋 및 푸시
git add .
git commit -m "민감 정보 제거 및 재커밋"
git push -u origin main