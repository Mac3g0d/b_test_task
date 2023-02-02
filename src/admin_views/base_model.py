from sqladmin import ModelView


class BaseModelView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    page_size = 50
    page_size_options = [50, 100, 200, 300]
