from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)

APP_INFO = Gauge(
    "app_info",
    "Application info (value=1)",
    ["app", "version", "environment"],
)


def observe_request(method: str, path: str, status_code: int, duration_seconds: float) -> None:
    HTTP_REQUESTS_TOTAL.labels(method=method, path=path, status=str(status_code)).inc()
    HTTP_REQUEST_DURATION_SECONDS.labels(method=method, path=path).observe(duration_seconds)


__all__ = [
    "APP_INFO",
    "observe_request",
    "generate_latest",
    "CONTENT_TYPE_LATEST",
]
