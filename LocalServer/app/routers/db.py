# app/routers/db.py
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
from app.utils import get_db_connection
import logging
import os
import csv

# 로깅 설정
logger = logging.getLogger("db")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [db] %(message)s",
    datefmt="%H:%M:%S"
)

router = APIRouter(tags=["db"])

class QueryReq(BaseModel):
    query: str

class QueryFileReq(QueryReq):
    filename: str

@router.get("/db/version", summary="DB 버전")
def db_version():
    logger.info("📡 DB 버전 요청 시작")
    print("📡 DB 버전 요청 시작")
    try:
        conn = get_db_connection()
        logger.debug("✅ DB 연결 성공")
        print("✅ DB 연결 성공")
        ver = conn.cursor().execute("SELECT @@VERSION").fetchone()[0]
        logger.debug(f"🧾 DB 버전: {ver}")
        print(f"🧾 DB 버전: {ver}")
        return {"version": ver}
    except Exception as e:
        logger.error(f"❌ DB 버전 조회 실패: {e}")
        print(f"❌ DB 버전 조회 실패: {e}")
        raise HTTPException(500, detail=str(e))
    finally:
        conn.close()

@router.get("/databases", summary="DB 목록", response_model=List[str])
def dbs():
    logger.info("📡 DB 목록 요청 시작")
    try:
        conn = get_db_connection()
        logger.debug("✅ DB 연결 성공")
    except Exception as e:
        logger.error(f"❌ DB 연결 실패: {e}")
        raise HTTPException(500, detail=f"DB 연결 실패: {str(e)}")
    try:
        rows = conn.cursor().execute("SELECT name FROM sys.databases").fetchall()
        dbs = [r[0] for r in rows]
        logger.debug(f"📂 DB 목록: {dbs}")
        return dbs
    finally:
        conn.close()

@router.get("/databases/{db}/tables", summary="테이블 목록", response_model=List[str])
def tables(db: str):
    logger.info(f"📡 테이블 목록 요청 - DB: {db}")
    try:
        conn = get_db_connection(db)
        logger.debug("✅ DB 연결 성공")
    except Exception as e:
        logger.error(f"❌ DB 연결 실패: {e}")
        raise HTTPException(404, detail=f"DB 연결 실패: {e}")
    try:
        rows = conn.cursor().execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
        ).fetchall()
        tables = [r[0] for r in rows]
        logger.debug(f"📄 테이블 목록: {tables}")
        return tables
    finally:
        conn.close()

@router.get("/databases/{db}/tables/{table}/columns", summary="컬럼 메타")
def columns(db: str, table: str):
    logger.info(f"📡 컬럼 메타 요청 - DB: {db}, 테이블: {table}")
    try:
        conn = get_db_connection(db)
        logger.debug("✅ DB 연결 성공")
        cur = conn.cursor()
        cur.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, 
                   CASE WHEN IS_NULLABLE = 'YES' THEN 1 ELSE 0 END AS is_nullable,
                   CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=?
        """, table)
        cols = [
            {
                "column_name": r.COLUMN_NAME,
                "data_type": r.DATA_TYPE,
                "is_nullable": bool(r.is_nullable),
                "character_maximum_length": r.CHARACTER_MAXIMUM_LENGTH
            }
            for r in cur.fetchall()
        ]
        if not cols:
            logger.warning("⚠️ 컬럼 정보 없음")
            raise HTTPException(404, detail="컬럼 정보 없음")
        logger.debug(f"📋 컬럼 메타: {cols}")
        return cols
    except Exception as e:
        logger.error(f"❌ 컬럼 메타 조회 실패: {e}")
        raise HTTPException(500, detail=str(e))
    finally:
        conn.close()

@router.post("/query", summary="SQL 쿼리 실행")
def run_query(req: QueryReq):
    logger.info("📡 SQL 쿼리 실행 요청")
    logger.debug(f"📝 쿼리 내용: {req.query}")
    try:
        conn = get_db_connection("STEAM_GAME")
        logger.debug("✅ DB 연결 성공")
        cur = conn.cursor()
        cur.execute(req.query)
        if cur.description:
            cols = [c[0] for c in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
            logger.debug(f"📊 결과 행 수: {len(rows)}")
        else:
            rows = []
            logger.debug("📭 결과 없음 (DML 등)")
        return {"rows": rows}
    except Exception as e:
        logger.error(f"❌ 쿼리 실행 실패: {e}")
        raise HTTPException(500, detail=f"쿼리 오류: {str(e)}")
    finally:
        conn.close()

@router.post("/query-to-file", summary="SQL 쿼리 실행 후 파일 저장")
def run_query_to_file(req: QueryFileReq):
    logger.info("📡 SQL 쿼리 실행 및 파일 저장 요청")
    logger.debug(f"📝 쿼리 내용: {req.query}")
    try:
        conn = get_db_connection("STEAM_GAME")
        logger.debug("✅ DB 연결 성공")
        cur = conn.cursor()
        cur.execute(req.query)
        os.makedirs("output", exist_ok=True)
        fp = os.path.join("output", req.filename)
        if cur.description:
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
            with open(fp, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(cols)
                writer.writerows(rows)
            logger.debug(f"📁 결과 저장 완료: {fp}")
            return {"result": "saved", "file": fp, "rows": len(rows)}
        else:
            with open(fp, "w", encoding="utf-8") as f:
                f.write("데이터 없음")
            logger.debug(f"📭 결과 없음, 파일 기록: {fp}")
            return {"result": "no_data", "file": fp}
    except Exception as e:
        logger.error(f"❌ 쿼리 실행 실패: {e}")
        raise HTTPException(500, detail=f"쿼리 오류: {str(e)}")
    finally:
        conn.close()
