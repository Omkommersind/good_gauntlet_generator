from django.db import models

from backend.db.models import BaseModel
from games.models import GameSettings
from users.models import UserModel


class GauntletModel(BaseModel):
    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True, blank=True)
    is_public = models.BooleanField(default=True)

    # Rules
    reroll_points_const = models.PositiveIntegerField(default=1)
    first_finished_points_award = models.PositiveIntegerField(default=3)

    class Meta:
        verbose_name = 'Gauntlet'
        verbose_name_plural = 'Gauntlets'


class GauntletStageModel(BaseModel, GameSettings):
    gauntlet = models.ForeignKey(GauntletModel, on_delete=models.CASCADE)
    prev = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='next')

    def __str__(self):
        return 'ID: %s (%s)' % (self.id, self.platform if self.platform else 'ANY')

    class Meta:
        verbose_name = 'Gauntlet stage'
        verbose_name_plural = 'Gauntlet stages'


class GauntletParticipantModel(BaseModel):
    gauntlet = models.ForeignKey(GauntletModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Gauntlet participant'
        verbose_name_plural = 'Gauntlet participants'
