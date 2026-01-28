import os
import time
import requests
from typing import Any
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.metrics import APP_INFO, CONTENT_TYPE_LATEST, generate_latest, observe_request

APP_NAME = os.getenv("APP_NAME", "jira-automation-dashboard")
APP_VERSION = os.getenv("APP_VERSION", "dev")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "").rstrip("/")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "")
JIRA_MAX_RESULTS = int(os.getenv("JIRA_MAX_RESULTS", "8"))

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


def jira_search_issues(max_results: int = 8) -> tuple[list[dict[str, Any]], str]:
    """
    Returns (issues, project_key). If Jira is not configured, returns ([], project_key).
    """
    if not (JIRA_BASE_URL and JIRA_EMAIL and JIRA_API_TOKEN and JIRA_PROJECT_KEY):
        return [], JIRA_PROJECT_KEY

    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    params = {
        "jql": f"project = {JIRA_PROJECT_KEY} ORDER BY created DESC",
        "maxResults": max_results,
        "fields": "summary,status,assignee",
    }

    r = requests.get(url, auth=auth, params=params, timeout=10)
    r.raise_for_status()

    issues: list[dict[str, Any]] = []
    for i in r.json().get("issues", []):
        key = i.get("key", "N/A")
        fields = i.get("fields") or {}
        status = (fields.get("status") or {}).get("name", "Unknown")
        assignee = (fields.get("assignee") or {}).get("displayName") or "Unassigned"

        issues.append(
            {
                "key": key,
                "summary": fields.get("summary", ""),
                "status": status,
                "assignee": assignee,
                "url": f"{JIRA_BASE_URL}/browse/{key}" if JIRA_BASE_URL else None,
            }
        )

    return issues, JIRA_PROJECT_KEY


@app.get("/health", response_class=JSONResponse)
def health():
    return {"status": "ok", "app": APP_NAME, "version": APP_VERSION, "environment": ENVIRONMENT}


@app.get("/jira/issues", response_class=JSONResponse)
def jira_issues():
    try:
        issues, _ = jira_search_issues(max_results=JIRA_MAX_RESULTS)
        return issues
    except requests.HTTPError as e:
        # удобно за debug в демо; не изкарвай secrets
        return JSONResponse(
            status_code=502,
            content={"error": "Jira API request failed", "details": str(e)},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Unexpected error", "details": str(e)},
        )


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # since the app is serving, we consider it "healthy" for UI purposes
    health_ok = True

    issues: list[dict[str, Any]] = []
    jira_project = JIRA_PROJECT_KEY

    try:
        issues, jira_project = jira_search_issues(max_results=JIRA_MAX_RESULTS)
    except Exception:
        # UI should still render even if Jira is unreachable/misconfigured
        issues = []

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": APP_NAME,
            "app_version": APP_VERSION,
            "environment": ENVIRONMENT,
            "health_ok": health_ok,
            "issues": issues,
            "jira_project": jira_project,
        },
    )


@app.get("/metrics")
def metrics():
    return HTMLResponse(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
