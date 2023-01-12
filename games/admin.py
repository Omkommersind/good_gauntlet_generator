from django.contrib import admin

from games.models import PlatformModel, GameModel


@admin.register(PlatformModel)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(GameModel)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
