
from django.contrib.admin.sites import AdminSite
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy
from django.db.models.base import ModelBase
from django.utils.text import capfirst


class GlazeAdminSite(AdminSite):
    # backport of some features from the django 1.7 release
    site_title = ugettext_lazy('Django site admin')
    site_header = ugettext_lazy('Django administration')
    index_title = ugettext_lazy('Site administration')

    site_links = ()
    extra_urls = ()

    def get_urls(self):
        return list(self.extra_urls) + super(GlazeAdminSite, self).get_urls()

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
