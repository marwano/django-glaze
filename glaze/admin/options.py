
from django.contrib.admin import ModelAdmin
from .urls import ProcessURLsMixin, MappedURLsMixin, ExtraURLsMixin


class BaseGlazeModelAdmin(ProcessURLsMixin, ModelAdmin):
    pass


class GlazeModelAdmin(BaseGlazeModelAdmin, MappedURLsMixin, ExtraURLsMixin):
    pass


class DisableDeleteMixin(object):
    def has_delete_permission(self, request, obj=None):
        return False


class DisableAddMixin(object):
    def has_add_permission(self, request, obj=None):
        return False
