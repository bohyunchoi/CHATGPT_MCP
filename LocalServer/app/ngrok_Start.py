from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
from pyngrok import conf, ngrok

# 로그 파일 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler("access.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

class LoggingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Hello"
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

        # 요청 로그 기록
        logging.info(f"{self.client_address[0]} {self.command} {self.path} {self.request_version}")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length else b''
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"POST OK")

        # 요청 로그 기록(POST)
        logging.info(f"{self.client_address[0]} {self.command} {self.path} {self.request_version} DATA={post_data[:200]!r}")

    def log_message(self, format, *args):
        # 기본 stdout 로그 대신 파일 로그로만 남기고 싶을 때
        pass

# 0.0.0.0 바인딩 필수!
server = HTTPServer(("0.0.0.0", 8000), LoggingHandler)


public_url = ngrok.connect(
    8000,                 # 로컬 포트
    domain="3on3.ngrok.app"  # 원하는 도메인(Reserved Domain이어야 함)
)
logging.info(f"ngrok tunnel: {public_url}")

try:
    logging.info("Starting server. Press Ctrl+C to stop.")
    server.serve_forever()
except KeyboardInterrupt:
    logging.info("Shutting down server...")
    server.server_close()
    ngrok.kill()
    logging.info("Server stopped cleanly.")
