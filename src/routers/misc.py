import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session

from ..utils import init

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck(request: Request, session: AsyncSession = Depends(get_session)) -> Response:
    await init(session)
    uptime = (datetime.now(tz=timezone.utc) - request.app.start_time).total_seconds()
    response = {
        "status": "OK",
        "uptime": f"{uptime:0.2f} seconds",
    }

    return Response(json.dumps(response))
