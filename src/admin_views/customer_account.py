from .base_model import BaseModelView
from models import CustomerAccount


class CustomerAccountAdmin(BaseModelView, model=CustomerAccount):
    name = 'Счет клиента'
    name_plural = 'Счета клиентов'

    column_list = (
        CustomerAccount.id, CustomerAccount.customer_id, CustomerAccount.currency_id
    )

    column_searchable_list = column_list
    column_sortable_list = column_list

