
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


CONSOLE_MIDDLEWARE = 'glaze.console.middleware.ConsoleMiddleware'


class BaseConsole(object):

    def __init__(self, storage, max_rows=10):
        self.storage = storage
        self.max_rows = max_rows

    def html_header(self):
        return ''

    def check_settings(self):
        if CONSOLE_MIDDLEWARE not in settings.MIDDLEWARE_CLASSES:
            template = "'%s' is not in your MIDDLEWARE_CLASSES setting."
            raise ImproperlyConfigured(template % CONSOLE_MIDDLEWARE)

    def write_html(self, val):
        self.check_settings()
        if not self.storage.html.getvalue():
            self.storage.html.write(self.html_header())
        self.storage.html.write(val)

    def write_js(self, val):
        self.check_settings()
        self.storage.js.write(val)
