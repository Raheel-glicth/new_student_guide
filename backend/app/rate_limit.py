import time
from collections import defaultdict, deque

from flask import current_app, jsonify, request


_REQUEST_BUCKETS = defaultdict(deque)


def _client_key():
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    ip_address = forwarded_for.split(",")[0].strip() if forwarded_for else request.remote_addr
    return f"{ip_address or 'local'}:{request.path}"


def register_rate_limits(app):
    @app.before_request
    def enforce_rate_limit():
        if not app.config["ENABLE_RATE_LIMITING"] or request.method == "OPTIONS":
            return None

        limit = app.config["RATE_LIMITS"].get(request.path)
        if not limit:
            return None

        now = time.time()
        window = app.config["RATE_LIMIT_WINDOW_SECONDS"]
        bucket = _REQUEST_BUCKETS[_client_key()]

        while bucket and bucket[0] <= now - window:
            bucket.popleft()

        if len(bucket) >= limit:
            current_app.logger.warning(
                "rate_limit_exceeded path=%s limit=%s window=%s",
                request.path,
                limit,
                window,
            )
            return (
                jsonify(
                    {
                        "error": "Too many requests. Please wait a minute and try again.",
                        "code": "rate_limited",
                    }
                ),
                429,
            )

        bucket.append(now)
        return None
