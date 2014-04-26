
from django.contrib.admin import ModelAdmin
from .urls import ProcessURLsMixin, MappedURLsMixin


class BaseGlazeModelAdmin(ProcessURLsMixin, ModelAdmin):
    pass


class GlazeModelAdmin(BaseGlazeModelAdmin, MappedURLsMixin):
    pass


class DisableDeleteMixin(object):
    def has_delete_permission(self, request, obj=None):
        return False
