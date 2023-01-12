from django.db.models import IntegerChoices


class DifficultiesEnum(IntegerChoices):
    EASY = 1
    NORMAL = 2
    HARD = 3


class LengthsEnum(IntegerChoices):
    SHORT = 1
    NORMAL = 2
    LONG = 3
