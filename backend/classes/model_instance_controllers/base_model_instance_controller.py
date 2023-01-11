from users.models import UserModel


class BaseModelInstanceController:
    model_class = None
    instance = None

    def __init__(self, instance):
        self.instance: UserModel = instance
        self.model_class = type(instance)
