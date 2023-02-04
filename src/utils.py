import logging
import random

import httpx
from fastapi.logger import logger


def setup_logger():
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    logger.handlers = gunicorn_error_logger.handlers


async def main():
    async with httpx.AsyncClient(base_url='http://localhost:8000') as client:
        for _ in range(500):
            r = await client.post('/api/v1/account_operations', json={
                "type": "d",
                "amount": random.randrange(0, 12345),
                "customer_account_id": "247ac096-5d56-4dcd-96aa-239b2474728e"}, follow_redirects=True)
            print(r.status_code)

if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
