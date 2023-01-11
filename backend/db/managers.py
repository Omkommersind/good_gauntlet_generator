from django.db.models.manager import BaseManager

from backend.db.querysets import SafeDeleteQuerySet, BaseCustomQuerySet


class BaseCustomManager(BaseManager.from_queryset(BaseCustomQuerySet)):
    def __init__(self, *args, **kwargs):
        super(BaseCustomManager, self).__init__(*args, **kwargs)


class SafeDeleteManager(BaseManager.from_queryset(SafeDeleteQuerySet)):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SafeDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if self.alive_only:
            return super().get_queryset(*args, **kwargs).filter(deleted_at=None)
        return super().get_queryset(*args, **kwargs)
