import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.db.models import BaseModel
from backend.utils import send_formatted_email
from users.querysets import UsersQuerySet


class UserModel(AbstractUser, BaseModel):
    first_name = None
    last_name = None
    activation_code = models.UUIDField(null=True, blank=True)

    objects = UsersQuerySet.as_manager()

    def __str__(self):
        if self.is_superuser:
            return '[S] %s' % self.username
        elif self.is_staff:
            return '[M] %s' % self.username
        return str(self.username)

    def save(self):
        # Todo: check if existing email with not activated account exists, if so - delete not activated account before
        pass

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


@receiver(post_save, sender=UserModel)
def user_to_inactive(sender, instance, created, update_fields, **kwargs):
    if created and not instance.is_superuser:
        instance.is_active = False
        code = uuid.uuid4()
        instance.activation_code = code
        instance.save()
        if instance.email:
            send_formatted_email('Confirmation code', 'registration/activation_email.html',
                                 {'code': str(code)}, [instance.email])


class JwtTokenModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False, blank=False)
    access_token = models.CharField(max_length=600, blank=False, null=False)
    refresh_token = models.CharField(max_length=600, blank=False, null=False)

    def __str__(self):
        return self.access_token

    class Meta:
        verbose_name = 'JWT token'
        verbose_name_plural = 'JWT tokens'
