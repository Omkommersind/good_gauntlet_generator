from rest_framework_simplejwt.tokens import RefreshToken

from users.models import UserModel, JwtTokenModel
from users.versions.v1.classes.DTO.user_auth_data import UserAuthData


class JwtTokenController:

    @staticmethod
    def generate_for_user(user: UserModel) -> UserAuthData:
        data = {}

        tokens = RefreshToken.for_user(user=user)
        data['access_token'] = str(tokens.access_token)
        data['refresh_token'] = str(tokens)
        JwtTokenModel.objects.get_or_create(
            user=user, **data
        )
        return UserAuthData(data['access_token'], data['refresh_token'])
