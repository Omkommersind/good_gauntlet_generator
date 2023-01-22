from django.db.models.manager import BaseManager

from backend.db.querysets import BaseCustomQuerySet


class BaseCustomManager(BaseManager.from_queryset(BaseCustomQuerySet)):
    def __init__(self, *args, **kwargs):
        super(BaseCustomManager, self).__init__(*args, **kwargs)
