from .base_model import BaseModelView
from models import AccountOperation


class AccountOperationAdmin(BaseModelView, model=AccountOperation):
    name = 'Операция по счету клиента'
    name_plural = 'Операции по счетам клиентов'

    column_list = (
        AccountOperation.id, AccountOperation.customer_account_id, AccountOperation.amount, AccountOperation.type
    )

    column_searchable_list = column_list
    column_sortable_list = column_list

