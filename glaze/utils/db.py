
from utile import bunch_or_dict
from django.db import connections, transaction


def get_rows(operation, parameters=(), alias='default'):
    cursor = connections[alias].cursor()
    cursor.execute(operation, parameters)
    columns = [i[0] for i in cursor.description]
    return [bunch_or_dict(zip(columns, row)) for row in cursor.fetchall()]


def db_execute(operation, parameters=(), alias='default'):
    ops = [operation] if isinstance(operation, basestring) else operation
    ops = [i for i in ops if i]
    for op in ops:
        cursor = connections[alias].cursor()
        cursor.execute(op, parameters)
        transaction.commit_unless_managed(using=alias)
