import logging
import time
from collections.abc import Callable
from typing import Any
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RouterLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log the request (HTTP method, endpoint path, client IP address)."""

    def __init__(self, app: ASGIApp, *, logger: logging.Logger) -> None:
        self._logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id: str = str(uuid4())
        logging_dict: dict[str, Any] = {"X-API-REQUEST-ID": request_id}
        request.state.request_id = request_id

        response, response_dict = await self._log_response(
            call_next, request, request_id
        )

        request_dict = await self._log_request(request)
        logging_dict["request"] = request_dict
        logging_dict["response"] = response_dict

        self._logger.info(logging_dict)

        return response

    async def _log_request(self, request: Request) -> dict:
        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"

        request_logging = {
            "method": request.method,
            "path": path,
            "ip": request.client.host if request.client else None,
        }

        return request_logging

    async def _log_response(
        self, call_next: Callable, request: Request, request_id: str
    ) -> tuple[Response, dict]:
        start_time = time.perf_counter()
        response = await self._execute_request(call_next, request, request_id)
        finish_time = time.perf_counter()

        overall_status = (
            "successful" if response and response.status_code < 400 else "failed"
        )
        execution_time = finish_time - start_time

        response_logging = {
            "status": overall_status,
            "status_code": response.status_code if response else 500,
            "time_taken": f"{execution_time:0.4f}s",
        }

        return response, response_logging

    async def _execute_request(
        self, call_next: Callable, request: Request, request_id: str
    ) -> Response:
        response: Response = await call_next(request)
        response.headers["X-API-Request-ID"] = request_id
        return response
