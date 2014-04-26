
from collections import namedtuple
from inspect import ismethod
from django.contrib.admin import ModelAdmin
from django.conf.urls import patterns, url, include
from utile import enforce

URLOptions = namedtuple('URLOptions', 'regex, name, admin_view, cacheable')


def admin_url(regex, name=None, admin_view=True, cacheable=False):
    def decorator(method):
        enforce(method.__name__.endswith('_view'),
                "%r method does not end with '_view'" % method.__name__)
        method.url = URLOptions(regex, name, admin_view, cacheable)
        return method
    return decorator


class MappedURLsMixin(object):

    def process_urls_mapped(self, urls):
        views = [getattr(self, i) for i in dir(self) if i.endswith('_view')]
        views = [i for i in views if ismethod(i) and hasattr(i, 'url')]
        new_urls = []
        site = self.admin_site if isinstance(self, ModelAdmin) else self
        for i in views:
            view = i
            if i.url.admin_view:
                view = site.admin_view(view, cacheable=i.url.cacheable)
            name = i.url.name
            if name and isinstance(self, ModelAdmin):
                name = name % self.model._meta.__dict__
            new_urls.append(url(regex=i.url.regex, view=view, name=name))
        return new_urls + urls


class ProcessURLsMixin(object):

    def get_urls(self):
        urls = super(ProcessURLsMixin, self).get_urls()
        names = [i for i in dir(self) if i.startswith('process_urls_')]
        processors = [getattr(self, i) for i in names]
        for processor in processors:
            urls = processor(urls)
        return urls
