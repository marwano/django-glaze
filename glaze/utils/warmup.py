
import sys
from os.path import dirname, join


def generate_django_warmup():
    before = set(sys.modules.keys())
    from django.conf import settings
    settings.configure()
    after = set(sys.modules.keys())
    names = sorted(set(after) - set(before))
    matches = []
    for i in names:
        path = getattr(sys.modules[i], '__file__', '')
        if not sys.modules[i] or i.startswith('_') or i.startswith('django'):
            continue
        if 'site-packages' in path or (path and 'lib/python' not in path):
            continue
        matches.append(i)
    print '\n'.join(matches)


def warmup(profile):
    path = join(dirname(__file__), 'files', 'warmup_%s.txt' % profile)
    modules = open(path).read().splitlines()
    map(__import__, modules)
