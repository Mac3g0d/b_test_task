import json
from collections.abc import Callable
from typing import Self

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.exceptions import ApiError


class ErrorMiddleware(BaseHTTPMiddleware):
    def __init__(
            self: Self,
            app: FastAPI,
    ) -> None:
        super().__init__(app)

    async def dispatch(self: Self, request: Request, call_next: Callable):  # noqa: ANN201
        try:
            return await call_next(request)
        except ApiError as e:
            return Response(json.dumps({"error": str(e)}), status_code=e.status_code)
