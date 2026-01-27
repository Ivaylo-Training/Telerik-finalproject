import os
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.metrics import APP_INFO, CONTENT_TYPE_LATEST, generate_latest, observe_request

APP_NAME = os.getenv("APP_NAME", "jira-automation-dashboard")
APP_VERSION = os.getenv("APP_VERSION", "dev")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

app = FastAPI(title="Jira Automation Dashboard", version="1.0.0")
templates = Jinja2Templates(directory="app/templates")

# Expose version/env via a gauge (Prometheus-friendly)
APP_INFO.labels(app=APP_NAME, version=APP_VERSION, environment=ENVIRONMENT).set(1)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    observe_request(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_seconds=time.time() - start,
    )
    return response


@app.get("/health", response_class=JSONResponse)
def health():
    return {"status": "ok", "app": APP_NAME, "version": APP_VERSION, "environment": ENVIRONMENT}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": APP_NAME, "app_version": APP_VERSION, "environment": ENVIRONMENT},
    )


@app.get("/metrics")
def metrics():
    return HTMLResponse(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
