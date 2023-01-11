from django.db import models
from rest_framework import status
from rest_framework.exceptions import APIException


class HTTPExceptions(models.IntegerChoices):
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST, 'Неверные данные в запросе'
    ENTITY_NOT_FOUND = status.HTTP_404_NOT_FOUND, 'Запись не найдена'
    PROFILE_NOT_FILLER = 550, 'Профиль не заполнен, необходимо открыть экран заполнения анкеты'
    INVALID_ACCESS_TOKEN = 551, 'Невалидный Firebase-токен'
    USER_IS_BLOCKED = 554, 'Пользователь заблокирован'
    FORM_COMPLETED = 555, 'Анкета уже заполнена'
    INVALID_CODE = 556, 'Неверный код'
    CODE_EXPIRED = 557, 'Срок действия кода подтверждения истек'
    INTERNAL_SERVER_ERROR = 500, 'Ошибка сервера'


class HTTPException(APIException):
    def __init__(self, exception: HTTPExceptions, reason=None):
        if reason:
            self.detail = {'reason': reason}
        else:
            self.detail = {'reason': exception.label}
        self.status_code = exception.value


class CustomHTTPException(APIException):
    def __init__(self, status: int, detail=None):
        if detail:
            self.detail = detail
        self.status_code = status


class InternalServerException(HTTPException):
    def __init__(self, reason=None):
        super().__init__(exception=HTTPExceptions.INTERNAL_SERVER_ERROR, reason=reason)


class EntityDoesNotExistException(HTTPException):
    def __init__(self, reason=None):
        super().__init__(exception=HTTPExceptions.ENTITY_NOT_FOUND, reason=reason)


class BadRequestException(HTTPException):
    def __init__(self, reason=None):
        super().__init__(exception=HTTPExceptions.BAD_REQUEST, reason=reason)


class ProfileNotFilledException(HTTPException):
    def __init__(self, reason=None):
        super().__init__(exception=HTTPExceptions.PROFILE_NOT_FILLER, reason=reason)


class BlockUserException(HTTPException):
    def __init__(self, reason=None):
        super().__init__(exception=HTTPExceptions.USER_IS_BLOCKED, reason=reason)


class InvalidFirebaseAuthException(HTTPException):
    def __init__(self, reason=None):
        super().__init__(exception=HTTPExceptions.INVALID_ACCESS_TOKEN, reason=reason)


class FormCompletedException(HTTPException):
    def __init__(self, reason=None):
        super().__init__(exception=HTTPExceptions.FORM_COMPLETED, reason=reason)


class InvalidCodeException(HTTPException):
    def __init__(self, reason=None):
        super().__init__(exception=HTTPExceptions.INVALID_CODE, reason=reason)


class CodeExpiredException(HTTPException):
    def __init__(self, reason=None):
        super().__init__(exception=HTTPExceptions.CODE_EXPIRED, reason=reason)
