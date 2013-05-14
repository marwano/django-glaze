
from django.contrib.admin.sites import AdminSite


class GlazeAdminSite(AdminSite):
    def get_urls(self):
        extra_urls = getattr(self, 'extra_urls', [])
        return extra_urls + super(GlazeAdminSite, self).get_urls()
