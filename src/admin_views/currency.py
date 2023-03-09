from models import Currency

from .base_model import BaseModelView


class CurrencyAdmin(BaseModelView, model=Currency):
    name = "Baлютa"
    name_plural = "Baлюты"

    column_list = (
        Currency.id, Currency.name, Currency.default,
    )

    column_searchable_list = column_list
    column_sortable_list = column_list

