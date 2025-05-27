@echo off
cd /d %~dp0

git add .
git commit -m "hello.py 업로드"
git push origin main

echo ✅ hello.py가 GitHub에 업로드되었습니다.