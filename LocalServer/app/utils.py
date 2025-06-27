# app/utils.py
import requests
import pyodbc
import time

def get_ngrok_url() -> str:
    """
    로컬 ngrok 관리 API에서 HTTPS 터널 URL을 가져옵니다.
    실패 시 localhost로 대체.
    """
    try:
        api_url = "http://127.0.0.1:4040/api/tunnels"
        resp = requests.get(api_url, timeout=2).json()
        for tunnel in resp.get("tunnels", []):
            url = tunnel.get("public_url", "")
            if url.startswith("https://"):
                return url
    except Exception:
        pass
    return "http://localhost:8000"

def get_db_connection(
    database: str = "master", *, retries: int = 3, delay: float = 1.0
):
    """Connect to SQL Server with simple retry logic."""
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=10.31.20.6;"
        f"DATABASE={database};"
        "UID=sa;PWD=f$ei#L!sa"
    )
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            conn = pyodbc.connect(conn_str, timeout=5)
            if attempt > 1:
                print(f"🔄 DB 연결 성공 - {attempt}회차 시도")
            return conn
        except pyodbc.Error as e:
            last_error = e
            print(f"⚠️ DB 연결 실패 {attempt}/{retries}: {e}")
            if attempt < retries:
                time.sleep(delay * attempt)
    raise last_error


#$env:MSSQL_SERVER = "10.31.20.6"
#$env:MSSQL_USER = "sa"
#$env:MSSQL_PASSWORD = "f$ei#L!sa"
#$env:MSSQL_DATABASE = "master"