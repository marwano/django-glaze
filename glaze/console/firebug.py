
import json
from pprint import pformat
from django.db import models
from django.core.serializers import serialize
from glaze.console.middleware import storage
from glaze.console.base import BaseConsole


class FirebugConsole(BaseConsole):

    def _call_method(self, method, arg):
        arg = json.dumps(str(arg))
        self.write_js('console.%s(%s);\n' % (method, arg))

    def log(self, obj):
        self._call_method('log', obj)

    def debug(self, obj):
        self._call_method('debug', obj)

    def info(self, obj):
        self._call_method('info', obj)

    def warn(self, obj):
        self._call_method('warn', obj)

    def error(self, obj):
        self._call_method('error', obj)

    def model_table(self, obj, title):
        rows = serialize('json', obj)
        self.write_js('console.group(%s);\n' % json.dumps(title))
        self.write_js('console.table(glaze_table(%s));\n' % rows)
        if hasattr(obj, 'query'):
            self.log(obj.query)
        self.write_js('console.groupEnd();\n')

    def dump(self, obj):
        if isinstance(obj, models.query.QuerySet):
            title = 'QuerySet: {0:,} row(s)'.format(obj.count())
            self.model_table(obj[0:self.max_rows], title)
        elif isinstance(obj, models.Model):
            self.model_table([obj], 'Model: %s' % obj._meta)
        else:
            self.log(pformat(obj))


console = FirebugConsole(storage)
