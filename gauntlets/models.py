from django.db import models

from backend.db.models import BaseModel
from users.models import UserModel


class GauntletModel(BaseModel):
    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    deadline = models.DateTimeField()

    reroll_points_const = models.PositiveIntegerField(default=1)
    first_finished_points_award = models.PositiveIntegerField(default=3)

    class Meta:
        verbose_name = 'Gauntlet'
        verbose_name_plural = 'Gauntlets'


class GauntletParticipantModel(BaseModel):
    gauntlet = models.ForeignKey(GauntletModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Gauntlet participant'
        verbose_name_plural = 'Gauntlet participants'
