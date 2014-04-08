
import threading
import json
from pprint import pformat
from django.db import models
from django.core.serializers import serialize


MAX_ROWS = 10
_data = threading.local()
_data.__dict__.setdefault('lines', '')


def _model_data(obj):
    data = json.loads(serialize('json', [obj]))[0]['fields']
    data['pk'] = obj.pk
    return data


def _model_table(rows):
    if rows:
        columns = sorted(_model_data(rows[0]).keys())
        columns = [dict(property=i, label=i) for i in columns]
        columns = json.dumps(columns)
        rows = json.dumps([_model_data(i) for i in rows])

        _data.lines += 'console.table(%s, %s);\n' % (rows, columns)


def log(obj):
    _data.lines += 'console.log(%s);\n' % json.dumps(str(obj))


def dump(obj):
    if isinstance(obj, models.query.QuerySet):
        title = 'QuerySet: {0:,} row(s)'.format(obj.count())
        _data.lines += 'console.group(%s);\n' % json.dumps(title)
        _model_table(obj[0:MAX_ROWS])
        _data.lines += 'console.groupEnd();\n'
    elif isinstance(obj, models.Model):
        title = 'Model: %s' % obj._meta
        _data.lines += 'console.group(%s);\n' % json.dumps(title)
        _model_table([obj])
        _data.lines += 'console.groupEnd();\n'
    else:
        log(pformat(obj))
