import logging
import random
from decimal import ROUND_HALF_EVEN, Decimal

from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from .models import AccountOperation, Currency, Customer, CustomerAccount


def setup_logger() -> None:
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    logger.handlers = gunicorn_error_logger.handlers


def round_decimal(numbers: Decimal, decimal_places: int) -> Decimal:
    return Decimal(numbers).quantize(
        Decimal(10) ** -decimal_places, ROUND_HALF_EVEN,
    )


async def init(session: AsyncSession) -> None:
    currency = Currency(name="USDT", default=True)
    cc = Currency(name="TonCoin", default=False)
    session.add(currency)
    session.add(cc)
    for _ in range(4):
        c = Customer(name="balbes" + str(random.randrange(1, 4)))
        cc = CustomerAccount(customer_id=c.id, currency_id=currency.id)
        session.add(c)
        session.add(cc)
        for _ in range(30):
            a = AccountOperation(amount=random.randrange(1, 500), type=random.choice(("d", "c")), customer_account_id=cc.id)
            session.add(a)
    await session.commit()


