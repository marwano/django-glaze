
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

    def dump(self, obj):
        if isinstance(obj, models.query.QuerySet):
            title = 'QuerySet: {0:,} row(s)'.format(obj.count())
            self.write_js('console.group(%s);\n' % json.dumps(title))
            data = serialize('json', obj[0:self.max_rows])
            self.write_js('console.table(glaze_table(%s));\n' % data)
            self.log(obj.query)
            self.write_js('console.groupEnd();\n')
        elif isinstance(obj, models.Model):
            title = 'Model: %s' % obj._meta
            self.write_js('console.group(%s);\n' % json.dumps(title))
            data = serialize('json', [obj])
            self.write_js('console.dir(glaze_table(%s)[0]);\n' % data)
            self.write_js('console.groupEnd();\n')
        else:
            self.log(pformat(obj))


console = FirebugConsole(storage)
