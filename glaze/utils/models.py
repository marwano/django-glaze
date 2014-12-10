
from django.conf import settings
from django.db.models import Model, ForeignKey


class UpdateMixin(object):
    def update(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])
        self.save()


class LabelMixin(object):
    label_format = u'{self.pk}'

    def __unicode__(self):
        return self.label_format.format(self=self)


def fieldset(fields, name=None, **field_options):
    fields = fields.split() if isinstance(fields, basestring) else fields
    return (name, dict(fields=fields, **field_options))


class CreatedByMixin(Model):
    created_by = ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True
