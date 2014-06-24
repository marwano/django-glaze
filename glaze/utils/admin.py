
from django.utils import six
from django.utils.text import capfirst


def foreign_list(*args):
    items = []
    for i in args:
        if isinstance(i, six.string_types) and '__' in i:
            names = i.split('__')
            accessor = lambda obj: reduce(getattr, names, obj)
            accessor.short_description = capfirst(names[-1].replace('_', ' '))
            accessor.admin_order_field = i
            items.append(accessor)
        else:
            items.append(i)
    return items
