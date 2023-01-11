from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import UserModel, JwtTokenModel


@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    list_display = ['id', 'username']
    search_fields = ('id', 'username')
    fieldsets = (
        (None, {
            'fields': ['name']
        }),
    )


@admin.register(JwtTokenModel)
class JwtTokenModelModel(admin.ModelAdmin):
    list_display = ['user', 'access_token']
