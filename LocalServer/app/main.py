# app/main.py
import yaml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response
from app.utils import get_ngrok_url
from app.routers import (
    file_ops, bat_ops, listing, github, db
)
from app.routers import mail

NGROK_URL = get_ngrok_url()

app = FastAPI(
    title="3on3 MCP File Pipeline",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    servers=[{"url":NGROK_URL}]
)

# 커스텀 OpenAPI
def custom_openapi():
    if app.openapi_schema: return app.openapi_schema
    schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
    schema["servers"] = [{"url":NGROK_URL}]
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi

@app.get("/openapi.yaml", include_in_schema=False)
def openapi_yaml():
    return Response(
      yaml.dump(app.openapi(), sort_keys=False),
      media_type="application/x-yaml"
    )
@app.middleware("http")
async def log_all_requests(request, call_next):
    try:
        print(f"📡 요청 수신: {request.method} {request.url}")
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"🔥 예외 발생: {e}")
        raise
        
# 라우터 등록
app.include_router(file_ops.router)
app.include_router(bat_ops.router)
app.include_router(listing.router)
app.include_router(github.router)
app.include_router(db.router)
app.include_router(mail.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)