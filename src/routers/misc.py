import json
from datetime import datetime

from fastapi import Request, Response, APIRouter


router = APIRouter()


@router.get("/healthcheck")
async def healthcheck(request: Request) -> Response:
    uptime = (datetime.now() - request.app.start_time).total_seconds()
    response = {
        "status": 'OK',
        "uptime": f'{uptime:0.2f} seconds',
    }

    return Response(json.dumps(response))
