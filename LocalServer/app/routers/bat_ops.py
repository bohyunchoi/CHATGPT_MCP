# app/routers/bat_ops.py
import os, subprocess, time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["bat"])
BASE_DIR = r"File\VibeCodeing"

class BatRunRequest(BaseModel):
    filename: str

@router.post("/run-bat", summary="로컬 BAT 실행")
def run_bat(req: BatRunRequest):
    fp = os.path.join(BASE_DIR, req.filename)
    if not os.path.exists(fp) or not fp.lower().endswith(".bat"):
        raise HTTPException(404, f"Not found: {fp}")
    start=time.time()
    p=subprocess.run(f'cmd /c "{fp}"', shell=True, capture_output=True, text=True)
    return {
      "result": "error" if p.returncode else "success",
      "stdout": p.stdout, "stderr": p.stderr,
      "return_code":p.returncode, "duration_sec":round(time.time()-start,4)
    }
