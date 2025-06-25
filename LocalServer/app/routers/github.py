# app/routers/github.py
import os, base64, requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["github"])
BASE_DIR = r"File\VibeCodeing"

class GitHubUpload(BaseModel):
    owner: str; repo: str; github_token: str
    local_path: str; repo_path: str; branch: str="main"

@router.post("/upload-to-github", summary="GitHub에 파일 업로드")
def upload(req: GitHubUpload):
    fp=os.path.join(BASE_DIR, req.local_path)
    if not os.path.exists(fp): raise HTTPException(404)
    data=base64.b64encode(open(fp,"rb").read()).decode()
    url=f"https://api.github.com/repos/{req.owner}/{req.repo}/contents/{req.repo_path}"
    hdr={"Authorization":f"token {req.github_token}"}
    payload={"message":f"upload {req.repo_path}","content":data,"branch":req.branch}
    r=requests.put(url,json=payload,headers=hdr)
    if r.status_code not in (200,201):
        raise HTTPException(r.status_code, r.json())
    return {"result":"success","details":r.json()}
