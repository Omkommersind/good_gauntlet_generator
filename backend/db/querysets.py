from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.exceptions import NotFound


class BaseCustomQuerySet(QuerySet):
    def get_with_raise(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            kwargs_string = ", ".join(f"{key}={value}" for key, value in kwargs.items())
            raise NotFound(f'{self.model.__name__} with {kwargs_string} not found')
        except self.model.MultipleObjectsReturned:
            return self.filter(*args, **kwargs).last()


class SafeDeleteQuerySet(BaseCustomQuerySet):
    def delete(self):
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return self.delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)

    def restore(self):
        self.update(deleted_at=None, is_active=True)
        return self
