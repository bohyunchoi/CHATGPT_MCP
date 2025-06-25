from app.utils import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.databases")
    for row in cursor.fetchall():
        print("📌 DB:", row[0])
    conn.close()
except Exception as e:
    print("❌ 오류:", e)