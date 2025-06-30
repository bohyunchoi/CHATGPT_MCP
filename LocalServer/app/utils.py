# app/utils.py
import os
import requests
import pyodbc
import time
import logging

# ─── 로거 설정 ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [utils] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("utils")

def get_ngrok_url(
    retries: int = 5,
    delay: float = 1.0,
    api_url: str = "http://127.0.0.1:4040/api/tunnels",
) -> str:
    """Return the HTTPS ngrok tunnel URL.

    An environment variable ``NGROK_URL`` can be set to bypass querying the
    local ngrok API. If the API is not reachable, a simple retry mechanism is
    used.  When no tunnel is found, ``http://localhost:8000`` is returned.
    """

    env_url = os.environ.get("NGROK_URL")
    if env_url:
        logger.info(f"🔌 Using NGROK_URL from environment: {env_url}")
        return env_url

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(api_url, timeout=2).json()
            for tunnel in resp.get("tunnels", []):
                url = tunnel.get("public_url", "")
                if url.startswith("https://"):
                    if attempt > 1:
                        logger.info(
                            f"🔌 Found ngrok URL after {attempt} attempts: {url}"
                        )
                    return url
        except Exception as e:
            logger.warning(
                f"⚠️ Failed to fetch ngrok URL ({attempt}/{retries}): {e}"
            )
        time.sleep(delay)

    fallback = "http://localhost:8000"
    logger.warning(f"⚠️ Using fallback URL: {fallback}")
    return fallback

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
