from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return (
            jsonify(
                {
                    "error": error.description,
                    "code": error.name.lower().replace(" ", "_"),
                }
            ),
            error.code,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("unhandled_exception")
        return (
            jsonify(
                {
                    "error": "Something went wrong. Please try again.",
                    "code": "internal_error",
                }
            ),
            500,
        )
