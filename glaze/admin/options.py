
from inspect import isclass
from django.contrib.admin import ModelAdmin
from django.utils.decorators import method_decorator
from glaze.utils.models import CreatedByMixin
from .urls import ProcessURLsMixin, MappedURLsMixin, ExtraURLsMixin
from .buttons import (SaveButton, SaveAsNewButton, SaveAddAnotherButton,
                      SaveContinueButton, DeleteButton)


class GlazeMediaMixin(object):
    class Media:
        js = ['glaze/js/admin.js']


class PreSaveModelMixin(object):
    def save_model(self, request, obj, form, change):
        names = [i for i in dir(self) if i.startswith('pre_save_model_')]
        methods = [getattr(self, i) for i in names]
        for method in methods:
            method(request, obj, form, change)
        super(PreSaveModelMixin, self).save_model(request, obj, form, change)


class SaveCreatedByMixin(object):
    def pre_save_model_created_by(self, request, obj, form, change):
        if not change and issubclass(obj.__class__, CreatedByMixin):
            obj.created_by = request.user


class SubmitRowMixin(object):
    buttons = (
        SaveButton(),
        DeleteButton(),
        SaveAsNewButton(),
        SaveAddAnotherButton(),
        SaveContinueButton(),
    )

    @property
    def change_form_template(self):
        info = self.model._meta.__dict__
        return [
            "admin/{app_label}/{model_name}/change_form.html".format(**info),
            "admin/{app_label}/change_form.html".format(**info),
            "glaze/change_form.html",
        ]

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        context['glaze_buttons'] = self.buttons
        return super(SubmitRowMixin, self).render_change_form(
            request, context, add, change, form_url, obj
        )

    def pre_save_model_buttons(self, request, obj, form, change):
        action = request.POST.get('glaze_action')
        valid_actions = [getattr(i, 'action', '') for i in self.buttons]
        method = getattr(self, action, None) if action else None
        if method and callable(method) and action in valid_actions:
            method(request, obj, form, change)


class GlazeModelAdmin(
        ProcessURLsMixin, MappedURLsMixin, ExtraURLsMixin, SaveCreatedByMixin,
        PreSaveModelMixin, GlazeMediaMixin, SubmitRowMixin, ModelAdmin):
    pass


class DisableDeleteMixin(object):
    def has_delete_permission(self, request, obj=None):
        return False


class DisableAddMixin(object):
    def has_add_permission(self, request, obj=None):
        return False
