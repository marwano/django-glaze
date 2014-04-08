
from django.utils.safestring import mark_safe
from glaze import console


class ConsoleMiddleware(object):
    def process_request(self, request):
        console._data.lines = ''

    def process_template_response(self, request, response):
        if console._data.lines and hasattr(response, 'context_data'):
            script = mark_safe('<script>%s</script>' % console._data.lines)
            response.context_data['glaze_console'] = script
        console._data.lines = ''
        return response
