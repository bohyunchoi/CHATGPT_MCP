# app/routers/listing.py
import os
from fastapi import APIRouter, HTTPException, Query
from typing import List

router = APIRouter(tags=["listing"])
BASE_DIR = r"File\VibeCodeing"

@router.get("/list-files", response_model=List[str])
def list_files(folder: str = Query(...)):
    fp=os.path.join(BASE_DIR, folder)
    if not os.path.isdir(fp): raise HTTPException(404)
    return [f for f in os.listdir(fp) if os.path.isfile(os.path.join(fp,f))]

@router.get("/list-folders", response_model=List[str])
def list_folders(folder: str = Query("")):
    fp=os.path.join(BASE_DIR, folder)
    if not os.path.isdir(fp): raise HTTPException(404)
    return [d for d in os.listdir(fp) if os.path.isdir(os.path.join(fp,d))]

@router.get("/list-python-files", response_model=List[str])
def list_py(folder: str = Query(...)):
    fp=os.path.join(BASE_DIR, folder)
    if not os.path.isdir(fp): raise HTTPException(404)
    return [f for f in os.listdir(fp) if f.endswith(".py")]
