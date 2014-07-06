
from django.utils.text import capfirst


def deslugify(text):
    return capfirst(text.replace('-', ' ').replace('_', ' '))
