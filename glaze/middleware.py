
import threading
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

GLOBAL_REQ_MW = 'glaze.middleware.GlobalRequestMiddleware'
_data = threading.local()


class GlobalRequestMiddleware(object):

    def process_request(self, request):
        _data.request = request


def get_request():
    if GLOBAL_REQ_MW not in settings.MIDDLEWARE_CLASSES:
        raise ImproperlyConfigured(
            "Put %r in your MIDDLEWARE_CLASSES setting in order to use "
            "global requests." % GLOBAL_REQ_MW
        )
    return _data.request
