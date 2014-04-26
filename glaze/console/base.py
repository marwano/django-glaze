
from django.contrib import messages
from django.utils.safestring import mark_safe
from glaze.middleware import get_request


class BaseConsole(object):

    def __init__(self, request=None, max_rows=10):
        self.request = request
        self.max_rows = max_rows

    def add_message(self, message, extra_tags=''):
        request = self.request or get_request()
        messages.add_message(request, messages.INFO, message, extra_tags)

    def add_html(self, html):
        self.add_message(mark_safe(html), 'glaze-console-html')

    def add_js(self, js):
        js = '<script type="text/javascript">%s</script>' % js
        self.add_message(mark_safe(js), 'glaze-console-js')
