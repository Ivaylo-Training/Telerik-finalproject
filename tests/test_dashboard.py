from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_index_page():
    r = client.get("/")
    assert r.status_code == 200
    assert "Jira Automation Dashboard" in r.text


def test_jira_issues_endpoint():
    r = client.get("/jira/issues")
    assert r.status_code in (200, 502)
