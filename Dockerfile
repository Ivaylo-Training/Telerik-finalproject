FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m appuser

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

USER appuser
EXPOSE 8000

ENV APP_NAME="jira-automation-dashboard" \
    ENVIRONMENT="dev" \
    APP_VERSION="dev"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
