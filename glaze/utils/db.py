
from utile import bunch_or_dict
from django.db import connections


def get_rows(sql, parameters=(), alias='default'):
    cursor = connections[alias].cursor()
    cursor.execute(sql, parameters)
    columns = [i[0] for i in cursor.description]
    return [bunch_or_dict(zip(columns, row)) for row in cursor.fetchall()]
