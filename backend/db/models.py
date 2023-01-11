from uuid import uuid4

from django.db import models
from django.utils import timezone

from backend.db.managers import SafeDeleteManager, BaseCustomManager


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    default_manager = BaseCustomManager()
    objects = BaseCustomManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.updated_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True


class SafeDeleteModel(BaseModel):
    default_manager = SafeDeleteManager()
    objects = SafeDeleteManager()
    all_objects = SafeDeleteManager(alive_only=False)

    class Meta:
        abstract = True


class SingletonModel(BaseModel):
    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)  # Todo
        return obj

    class Meta:
        abstract = True
