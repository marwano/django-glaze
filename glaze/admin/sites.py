
from django.contrib.admin import AdminSite
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy
from django.db.models.base import ModelBase
from django.conf.urls import patterns, url, include
from django.utils.text import capfirst
from django.conf import settings
from django.utils.cache import patch_response_headers
from django.views.decorators.cache import cache_page
from .urls import ProcessURLsMixin, MappedURLsMixin, ExtraURLsMixin


class SiteLinksMixin(object):
    site_links = ()

    def prepare_site_links(self):
        links = list(self.site_links)
        if not links:
            links = list(self._registry)
            links.sort(key=lambda i: i._meta.verbose_name_plural.lower())

        for key, val in enumerate(links):
            if isinstance(val, ModelBase):
                info = (val._meta.app_label, val._meta.model_name)
                viewname = 'admin:%s_%s_changelist' % info
                url = reverse_lazy(viewname, current_app=self.name)
                label = capfirst(val._meta.verbose_name_plural)
                links[key] = (url, label)
        return links


class GlazeAdminSite(ProcessURLsMixin, MappedURLsMixin, ExtraURLsMixin,
                     SiteLinksMixin, AdminSite):

    def each_context(self, request):
        context = super(GlazeAdminSite, self).each_context(request)
        context['prepared_site_links'] = self.prepare_site_links()
        return context
