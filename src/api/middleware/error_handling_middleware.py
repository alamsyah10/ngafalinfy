import logging
from collections.abc import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.config import settings
from src.domain.error.base import ApplicationError


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to centrally handle `ApplicationError` and other errors
    that occur during API request processing, and return a standardized
    error response in JSON format
    """

    def __init__(self, app: ASGIApp, *, logger: logging.Logger) -> None:
        self._logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response: Response = await call_next(request)
        except ApplicationError as e:
            # custom error
            self._logger.error(e, exc_info=True)
            response = JSONResponse(
                content={
                    "status": e.status,
                    "code": e.code,
                    "message": e.message,
                },
                status_code=e.status,
                headers={
                    "Access-Control-Allow-Origin": settings.CORS_ALLOW_ORIGINS,
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Expose-Headers": "*",
                },
            )
        except Exception as e:
            # unexpected error
            self._logger.exception(e, exc_info=True)
            response = JSONResponse(
                content={
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "code": "unexpected_error",
                    "message": e.__str__(),
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                headers={
                    "Access-Control-Allow-Origin": settings.CORS_ALLOW_ORIGINS,
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Expose-Headers": "*",
                },
            )
        return response
