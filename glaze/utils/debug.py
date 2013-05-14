
from os.path import dirname, join
import django.views.debug

CUSTOM_500_PATH = join(dirname(__file__), 'templates', 'custom_500.html')


def customize_500_template():
    template = django.views.debug.TECHNICAL_500_TEMPLATE
    if 'GLAZE CUSTOMIZATIONS' not in template:
        old, new = '</head>', open(CUSTOM_500_PATH).read() + '</head>'
        django.views.debug.TECHNICAL_500_TEMPLATE = template.replace(old, new)
