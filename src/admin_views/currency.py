from .base_model import BaseModelView
from models import Currency


class CurrencyAdmin(BaseModelView, model=Currency):
    name = 'Валюта'
    name_plural = 'Валюты'

    column_list = (
        Currency.id, Currency.name, Currency.default
    )

    column_searchable_list = column_list
    column_sortable_list = column_list

