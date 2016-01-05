from django.contrib.staticfiles import storage


class ForcedCachedStaticFilesStorage(storage.CachedStaticFilesStorage):
    def url(self, name, force=True):
        return super(ForcedCachedStaticFilesStorage, self).url(name, force)


class ForcedManifestStaticFilesStorage(storage.ManifestStaticFilesStorage):
    def url(self, name, force=True):
        return super(ForcedManifestStaticFilesStorage, self).url(name, force)
