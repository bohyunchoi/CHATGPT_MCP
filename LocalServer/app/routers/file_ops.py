# app/routers/file_ops.py

import os
import subprocess
import time
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal

# ─── 로거 설정 ───────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [file_ops] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("file_ops")

# ─── 기본 디렉토리 ───────────────────────────────────────────────────────────
BASE_DIR = r"File"

router = APIRouter(
    prefix="/file",
    tags=["file"],
    responses={404: {"description": "Not found"}, 400: {"description": "Invalid request"}}
)

class FileRequest(BaseModel):
    action:   Literal["read", "write", "modify"]
    filename: str
    content:  str = ""
    find:     str = ""
    replace:  str = ""

@router.post("", summary="파일 읽기/쓰기/수정/실행")
async def file_read_write(req: FileRequest):
    print(f"📥 요청 수신: action={req.action}, filename={req.filename!r}")
    logger.info(f"🔔 Incoming request: action={req.action}, filename={req.filename!r}")
    logger.debug(f"BASE_DIR = {BASE_DIR!r}")

    # 1) 경로 계산
    fp = os.path.normpath(os.path.join(BASE_DIR, req.filename))
    print(f"📁 파일 경로: {fp}")
    logger.debug(f"Resolved filepath: {fp!r}")

    # 2) 폴더 생성
    dirpath = os.path.dirname(fp) or BASE_DIR
    print(f"📂 디렉토리 확인 및 생성: {dirpath}")
    logger.debug(f"Ensuring directory exists: {dirpath!r}")
    os.makedirs(dirpath, exist_ok=True)

    # 3) WRITE
    if req.action == "write":
        print("✏️ 파일 쓰기 작업 시작")
        logger.info("✏️  Write operation")
        try:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(req.content)
            print(f"✅ 파일 작성 완료: {fp}")
            logger.info(f"✅ File written: {fp!r}")
            return {"result": f"File written: {fp}"}
        except Exception as e:
            print(f"❌ 파일 쓰기 오류: {e}")
            logger.error(f"❌ Write failed: {e}")
            raise HTTPException(status_code=500, detail=f"Write error: {e}")

    # 4) 존재 확인 (READ/MODIFY 전용)
    exists = os.path.exists(fp)
    print(f"🔍 파일 존재 여부: {exists}")
    logger.debug(f"File exists? {exists}")
    if not exists:
        print(f"⚠️ 파일이 존재하지 않음: {fp}")
        logger.warning(f"⚠️ File not found: {fp!r}")
        raise HTTPException(status_code=404, detail=f"Not found: {fp}")

    # 5) READ
    if req.action == "read":
        print("📖 파일 읽기 시작")
        logger.info("📖 Read operation")
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = f.read()
            print(f"✅ 읽기 완료: {len(data)} bytes")
            logger.info(f"✅ Read successful: {len(data)} bytes")
            return {"result": data}
        except Exception as e:
            print(f"❌ 파일 읽기 오류: {e}")
            logger.error(f"❌ Read failed: {e}")
            raise HTTPException(status_code=500, detail=f"Read error: {e}")

    # 6) MODIFY
    if req.action == "modify":
        print(f"🔄 파일 수정 작업: '{req.find}' → '{req.replace}'")
        logger.info(f"🔄 Modify operation: find={req.find!r} replace={req.replace!r}")
        try:
            with open(fp, "r", encoding="utf-8") as f:
                txt = f.read()
            if req.find not in txt:
                print(f"❌ 찾을 문자열 없음: '{req.find}'")
                logger.warning(f"🔍 '{req.find}' not found in file")
                raise HTTPException(status_code=404, detail=f"'{req.find}' not found in file")
            updated = txt.replace(req.find, req.replace)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(updated)
            print("✅ 파일 수정 완료")
            logger.info("✅ Modify successful")
            return {"result": f"File modified: {fp}"}
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ 수정 중 오류 발생: {e}")
            logger.error(f"❌ Modify failed: {e}")
            raise HTTPException(status_code=500, detail=f"Modify error: {e}")

    # 7) .py 실행
    if fp.endswith(".py"):
        print(f"▶️ 파이썬 파일 실행: {fp}")
        logger.info("▶️ Python execution")
        start = time.time()
        proc = subprocess.run(["python", fp], capture_output=True, text=True)
        duration = round(time.time() - start, 4)
        if proc.returncode != 0:
            print(f"❌ 실행 오류 (코드 {proc.returncode})")
            logger.error(f"❌ Execution error (code {proc.returncode})")
            logger.debug(f"stderr:\n{proc.stderr}")
            return {
                "result": "Execution error",
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "duration_sec": duration
            }
        print(f"✅ 실행 성공 ({duration}s)")
        logger.info(f"✅ Execution success in {duration}s")
        logger.debug(f"stdout:\n{proc.stdout}")
        return {
            "result": "Execution success",
            "stdout": proc.stdout,
            "duration_sec": duration
        }

    # 8) 잘못된 action
    print(f"❓ 잘못된 요청: action={req.action}")
    logger.warning(f"❓ Invalid action requested: {req.action!r}")
    raise HTTPException(status_code=400, detail="Invalid action")
