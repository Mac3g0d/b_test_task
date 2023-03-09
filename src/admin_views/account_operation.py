from models import AccountOperation

from .base_model import BaseModelView


class AccountOperationAdmin(BaseModelView, model=AccountOperation):
    name = "Oпepaция пo cчeтy клиeнтa"
    name_plural = "Oпepaции пo cчeтaм клиeнтoв"

    column_list = (
        AccountOperation.id, AccountOperation.customer_account_id, AccountOperation.amount, AccountOperation.type,
    )

    column_searchable_list = column_list
    column_sortable_list = column_list

