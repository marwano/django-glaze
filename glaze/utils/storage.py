
from django.contrib.staticfiles.storage import CachedStaticFilesStorage

class ForcedCachedStaticFilesStorage(CachedStaticFilesStorage):

    def url(self, name, force=True):
        return super(ForcedCachedStaticFilesStorage, self).url(name, force)

