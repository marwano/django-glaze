
from functools import partial
from django.utils import six
from glaze.utils.text import deslugify


def _get_foreign_field_value(obj, names):
    return reduce(getattr, names, obj)


def foreign_fields(*fields):
    items = []
    for field in fields:
        if isinstance(field, six.string_types) and '__' in field:
            names = field.split('__')
            func = partial(_get_foreign_field_value, names=names)
            func.__name__ = names[-1]
            func.short_description = deslugify(names[-1])
            func.admin_order_field = field
            items.append(func)
        else:
            items.append(field)
    return items
