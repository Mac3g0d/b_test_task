from models import Customer

from .base_model import BaseModelView


class CustomerAdmin(BaseModelView, model=Customer):
    name = "Kлиeнт"
    name_plural = "Kлиeнты"

    column_list = (
        Customer.id, Customer.name,
    )

    column_searchable_list = column_list
    column_sortable_list = column_list

