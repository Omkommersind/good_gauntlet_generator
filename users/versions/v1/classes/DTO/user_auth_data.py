from backend.classes.DTO.base_data_transfer_object_class import BaseDTO


class UserAuthData(BaseDTO):
    __slots__ = ['access_token', 'refresh_token']

    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
