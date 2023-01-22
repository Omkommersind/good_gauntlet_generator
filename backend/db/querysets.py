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
