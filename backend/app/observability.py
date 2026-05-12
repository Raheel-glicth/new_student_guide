import logging
import time
import uuid

from flask import g, request


def configure_logging(app):
    if app.logger.handlers:
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def register_observability(app):
    @app.before_request
    def attach_request_context():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        g.request_started_at = time.perf_counter()

    @app.after_request
    def add_request_metadata(response):
        response.headers["X-Request-ID"] = getattr(g, "request_id", "")
        response.headers["X-App-Version"] = app.config["APP_VERSION"]

        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")

        if app.config["ENABLE_REQUEST_LOGGING"] and request.path.startswith("/api"):
            duration_ms = int(
                (time.perf_counter() - getattr(g, "request_started_at", time.perf_counter()))
                * 1000
            )
            app.logger.info(
                "request_complete method=%s path=%s status=%s duration_ms=%s request_id=%s",
                request.method,
                request.path,
                response.status_code,
                duration_ms,
                getattr(g, "request_id", ""),
            )

        return response
