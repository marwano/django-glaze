

class UpdateMixin(object):
    def update(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])
        self.save()


def choices(items):
    return tuple((i, i) for i in items.split())


def make_fieldset(fields, name=None):
    fields = fields.split() if isinstance(fields, basestring) else fields
    return (name, dict(fields=fields))
