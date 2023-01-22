from django.db import models

from backend.db.models import BaseModel
from games.enums import DifficultiesEnum, LengthsEnum
from users.models import UserModel


class PlatformModel(BaseModel):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Platform'
        verbose_name_plural = 'Platforms'


class GameSettings(models.Model):
    platform = models.ForeignKey(PlatformModel, on_delete=models.CASCADE, null=True, blank=True)
    difficulty = models.PositiveIntegerField(choices=DifficultiesEnum.choices, default=DifficultiesEnum.NORMAL)
    length = models.PositiveIntegerField(choices=LengthsEnum.choices, default=LengthsEnum.NORMAL)

    class Meta:
        abstract = True


class GameModel(BaseModel, GameSettings):
    title = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'


class DifficultyFeedbackModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    game = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(choices=DifficultiesEnum.choices, default=DifficultiesEnum.NORMAL)

    class Meta:
        verbose_name = 'Difficulty feedback'
        verbose_name_plural = 'Difficulty feedback'


class LengthFeedbackModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    game = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(choices=LengthsEnum.choices, default=LengthsEnum.NORMAL)

    class Meta:
        verbose_name = 'Length feedback'
        verbose_name_plural = 'Length feedback'
