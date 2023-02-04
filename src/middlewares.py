import json

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.exceptions import ApiException


class ErrorMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ApiException as e:
            return Response(json.dumps({'error': str(e)}), status_code=e.status_code)