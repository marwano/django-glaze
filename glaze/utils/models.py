
from django.forms.models import model_to_dict


class UpdateMixin(object):
    def update(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])
        self.save()


class LabelMixin(object):
    label_format = '%(pk)s'

    def __unicode__(self):
        data = model_to_dict(self)
        data['pk'] = self.pk
        return self.label_format % data


def fieldset(fields, name=None, **field_options):
    fields = fields.split() if isinstance(fields, basestring) else fields
    return (name, dict(fields=fields, **field_options))
