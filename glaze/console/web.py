
from collections import OrderedDict
from random import randrange
from pprint import pformat
from django.db import models
from django.utils.html import escape
from django.template import loader, Context
from django.forms.models import model_to_dict
from .base import BaseConsole

try:
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import HtmlFormatter
except ImportError:
    highlight = None


def brief_model(obj):
    data = model_to_dict(obj)
    pk = obj._meta.pk.name
    no_pk_data = [(k, v) for k, v in data.items() if k != pk]
    return OrderedDict([(pk, data[pk])] + sorted(no_pk_data))


def detailed_model(obj):
    names = sorted(dir(obj), key=lambda s: s.lower())
    data = OrderedDict()
    for name in names:
        try:
            data[name] = pformat(getattr(obj, name, None))
        except Exception as err:
            data[name] = pformat(err)
    return data


class WebConsole(BaseConsole):
    query_set_template = 'glaze/console_query_set.html'
    model_template = 'glaze/console_model.html'

    def log(self, obj):
        self.add_html('<pre>%s</pre>' % escape(obj))

    def template(self, name, context):
        self.add_html(loader.get_template(name).render(Context(context)))

    def dump(self, obj):
        if isinstance(obj, models.query.QuerySet):
            count = '{:,}'.format(obj.count())
            rows = [brief_model(i) for i in obj[0:self.max_rows]]
            context = dict(obj=obj, rows=rows, count=count)
            self.template(self.query_set_template, context)
        elif isinstance(obj, models.Model):
            context = {}
            context['brief'] = brief_model(obj)
            context['detailed'] = detailed_model(obj)
            context['model_name'] = obj._meta
            context['id'] = 'glaze-%s' % randrange(1000000)
            self.template(self.model_template, context)
        else:
            if highlight:
                html = highlight(pformat(obj), PythonLexer(), HtmlFormatter())
            else:
                html = '<pre>%s</pre>' % escape(pformat(obj))
            self.add_html(html)


console = WebConsole()
