from .base_model import BaseModelView
from models import Customer


class CustomerAdmin(BaseModelView, model=Customer):
    name = 'Клиент'
    name_plural = 'Клиенты'

    column_list = (
        Customer.id, Customer.name
    )

    column_searchable_list = column_list
    column_sortable_list = column_list

