
import hashlib
from django.contrib.admin.sites import AdminSite
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy
from django.db.models.base import ModelBase
from django.conf.urls import patterns, url, include
from django.utils.text import capfirst
from django.conf import settings
from django.utils.cache import patch_response_headers
from django.views.decorators.cache import cache_page

TEN_YEARS = 60*60*24*365*10


class GlazeAdminSite(AdminSite):
    # backport of some features from the django 1.7 release
    site_title = ugettext_lazy('Django site admin')
    site_header = ugettext_lazy('Django administration')
    index_title = ugettext_lazy('Site administration')

    site_links = ()
    extra_urls = ()
    jsi18n_hash = None

    def get_urls(self):
        urls = super(GlazeAdminSite, self).get_urls()
        if not settings.USE_I18N:
            urls = [i for i in urls if getattr(i, 'name', '') != 'jsi18n']

            if not self.jsi18n_hash:
                js = self.i18n_javascript(None).content
                self.jsi18n_hash = hashlib.md5(js).hexdigest()[:12]

            pattern = r'^jsi18n_cache/%s$' % self.jsi18n_hash
            view = self.admin_view(self.i18n_javascript, cacheable=True)
            view = cache_page(TEN_YEARS)(view)
            urls.append(url(pattern, view, name='jsi18n'))

        return list(self.extra_urls) + urls

    def prepare_site_links(self):
        links = list(self.site_links)
        if not links:
            links = list(self._registry)
            links.sort(key=lambda i: i._meta.verbose_name_plural.lower())

        for key, val in enumerate(links):
            if isinstance(val, ModelBase):
                info = (val._meta.app_label, val._meta.model_name)
                viewname = 'admin:%s_%s_changelist' % info
                url = reverse(viewname, current_app=self.name)
                label = capfirst(val._meta.verbose_name_plural)
                links[key] = (url, label)
        return links
