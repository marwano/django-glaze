
import threading
from StringIO import StringIO

storage = threading.local()


class ConsoleMiddleware(object):

    def process_request(self, request):
        storage.html = StringIO()
        storage.js = StringIO()

    def process_template_response(self, request, response):
        ctx = getattr(response, 'context_data', None)
        if ctx:
            ctx['glaze_console_html'] = storage.html.getvalue()
            ctx['glaze_console_js'] = storage.js.getvalue()
        del storage.html, storage.js
        return response
