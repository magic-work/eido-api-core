
import requests
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.logs import get_logger
from app.settings import get_settings

settings = get_settings()
logger = get_logger(__name__)


async def handle_uncaught_exceptions(request: Request, call_next: callable):
    """Send a message to Slack when an uncaught exception occurs"""
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(e)
        if settings.slack_webhook_url:
            text = f"[{settings.app_title}] Uncaught Exception: {e}"
            requests.post(settings.slack_webhook_url, json={"text": text}, timeout=5, headers={'Content-Type': 'application/json'})
        response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "An uncaught exception occurred"})
    return response


async def handle_validation_error(request: Request, exc: RequestValidationError):
    """Exception handler to get more information about 422 errors. Not technically invoked as middleware, but acts as such."""
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logger.error(f"{request}: {exc_str}")
    content = {'status_code': 422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=422)
