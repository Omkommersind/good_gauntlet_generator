from django.contrib import admin

from gauntlets.models import GauntletModel, GauntletParticipantModel


@admin.register(GauntletModel)
class GauntletAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'creator']


@admin.register(GauntletParticipantModel)
class GauntletParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'gauntlet']
