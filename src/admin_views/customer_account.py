from models import CustomerAccount

from .base_model import BaseModelView


class CustomerAccountAdmin(BaseModelView, model=CustomerAccount):
    name = "Cчeт клиeнтa"
    name_plural = "Cчeтa клиeнтoв"

    column_list = (
        CustomerAccount.id, CustomerAccount.customer_id, CustomerAccount.currency_id,
    )

    column_searchable_list = column_list
    column_sortable_list = column_list

