
from django.template.loader import render_to_string
from glaze.utils.text import deslugify


class Button(object):
    template_name = None
    show_if = ()

    def __init__(self, show_if=(), template_name=None):
        self.show_if = show_if or self.show_if
        self.template_name = template_name or self.template_name

    def is_shown(self, context):
        return all(func(context) for func in self.show_if)

    def render(self, context):
        context['button'] = self
        if self.is_shown(context):
            return render_to_string(self.template_name, None, context)
        else:
            return ''


class SaveButton(Button):
    template_name = 'glaze/buttons/save.html'


class SaveAsNewButton(Button):
    template_name = 'glaze/buttons/save_as_new.html'


class SaveAddAnotherButton(Button):
    template_name = 'glaze/buttons/save_add_another.html'


class SaveContinueButton(Button):
    template_name = 'glaze/buttons/save_continue.html'


class DeleteButton(Button):
    template_name = 'glaze/buttons/delete.html'


class SimpleSaveButton(Button):
    template_name = 'glaze/buttons/simple_save.html'


class CloseButton(Button):
    template_name = 'glaze/buttons/close.html'


class LinkButton(Button):
    template_name = 'glaze/buttons/link.html'

    def __init__(self, url_name, label=None, show_if=(), template_name=None):
        super(LinkButton, self).__init__(show_if, template_name)
        self.url_name = url_name
        self.label = label or deslugify(url_name)


class ActionButton(Button):
    template_name = 'glaze/buttons/action.html'

    def __init__(self, action, label=None, show_if=(), template_name=None):
        super(ActionButton, self).__init__(show_if, template_name)
        self.action = action
        self.label = label or deslugify(action)


def is_saved(context):
    return context['change']


def is_new(context):
    return context['add']
