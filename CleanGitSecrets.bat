@echo off
cd /d %~dp0

REM GitHubPush.bat을 캐시에서 제거
git rm --cached GitHubPush.bat

REM 민감 정보 제거 커밋
git commit -m "GitHubPush.bat 제거 (민감 정보 포함)"

REM 원격 저장소로 푸시
git push -u origin main

REM 사용자 안내 메시지
echo 민감 정보가 포함된 GitHubPush.bat을 커밋 기록에서 제거하고 푸시했습니다.
echo GitHub에서 푸시가 허용되는지 확인하세요.