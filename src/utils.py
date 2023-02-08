import logging
import random

import httpx
from fastapi.logger import logger

from .models import Customer, Currency, CustomerAccount, AccountOperation


def setup_logger():
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    logger.handlers = gunicorn_error_logger.handlers


async def init(session):
    currency = Currency(name='USDT', default=True)
    cc = Currency(name='TonCoin', default=False)
    session.add(currency)
    session.add(cc)
    for _ in range(4):
        c = Customer(name='balbes' + str(random.randrange(1, 4)))
        cc = CustomerAccount(customer_id=c.id, currency_id=currency.id)
        session.add(c)
        session.add(cc)
        for _ in range(30):
            a = AccountOperation(amount=random.randrange(1, 500), type=random.choice(('d', 'c')), customer_account_id=cc.id)
            session.add(a)
    await session.commit()


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
