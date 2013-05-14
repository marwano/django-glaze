
from django.conf import settings
from utile import dir_dict

globals().update(dir_dict(settings))
