from django.contrib.auth.models import AbstractUser
from django.db import models

from backend.db.models import BaseModel
from users.versions.v1.querysets import UsersQuerySet


class UserModel(AbstractUser, BaseModel):
    first_name = None
    last_name = None

    default_manager = UsersQuerySet.as_manager()
    objects_v1 = UsersQuerySet.as_manager()

    def __str__(self):
        if self.is_superuser:
            return '[S] %s' % self.username
        elif self.is_staff:
            return '[M] %s' % self.username
        return str(self.username)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class JwtTokenModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False, blank=False)
    access_token = models.CharField(max_length=600, blank=False, null=False)
    refresh_token = models.CharField(max_length=600, blank=False, null=False)

    def __str__(self):
        return self.access_token

    class Meta:
        verbose_name = 'JWT token'
        verbose_name_plural = 'JWT tokens'
