
from collections import namedtuple
from inspect import ismethod
from django.contrib.admin import ModelAdmin
from django.conf.urls import patterns, url, include
from utile import enforce


class AdminURL(object):
    def __init__(self, regex, view=None, kwargs=None, name=None,
                 admin_view=True, cacheable=False):
        self.regex = regex
        self.view = view
        self.kwargs = kwargs
        self.name = name
        self.admin_view = admin_view
        self.cacheable = cacheable

    def get_url(self, obj, view=None):
        site = obj.admin_site if isinstance(obj, ModelAdmin) else obj
        view = view or self.view
        if self.admin_view:
            view = site.admin_view(view, cacheable=self.cacheable)
        name = self.name
        if name and isinstance(obj, ModelAdmin):
            name = name.format(**obj.model._meta.__dict__)
        return url(self.regex, view, self.kwargs, name)


def map_admin_url(regex, name=None, admin_view=True, cacheable=False):
    def decorator(method):
        enforce(method.__name__.endswith('_view'),
                "%r method does not end with '_view'" % method.__name__)
        method.admin_url = AdminURL(regex, name=name, admin_view=admin_view,
                                    cacheable=cacheable)
        return method
    return decorator


class MappedURLsMixin(object):
    def process_urls_mapped(self, urls):
        views = [getattr(self, i) for i in dir(self) if i.endswith('_view')]
        views = [i for i in views if ismethod(i) and hasattr(i, 'admin_url')]
        new_urls = [i.admin_url.get_url(self, i) for i in views]
        return new_urls + urls


class ExtraURLsMixin(object):
    extra_urls = ()

    def process_urls_extra(self, urls):
        new_urls = []
        for i in self.extra_urls:
            i = i.get_url(self) if isinstance(i, AdminURL) else i
            new_urls.append(i)
        return new_urls + urls


class ProcessURLsMixin(object):
    def get_urls(self):
        urls = super(ProcessURLsMixin, self).get_urls()
        names = [i for i in dir(self) if i.startswith('process_urls_')]
        processors = [getattr(self, i) for i in names]
        for processor in processors:
            urls = processor(urls)
        return urls
