from django.contrib import admin

from gauntlets.models import GauntletModel, GauntletParticipantModel, GauntletStageModel


@admin.register(GauntletStageModel)
class GauntletStageAdmin(admin.ModelAdmin):
    list_display = ['id', 'gauntlet', 'platform', 'difficulty', 'length']


class GauntletStageInline(admin.TabularInline):
    model = GauntletStageModel
    fields = ['id', 'platform', 'difficulty', 'length', 'prev']
    extra = 0


@admin.register(GauntletModel)
class GauntletAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'creator']
    inlines = [GauntletStageInline]


@admin.register(GauntletParticipantModel)
class GauntletParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'gauntlet']
