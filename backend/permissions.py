from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from backend.exceptions import BlockUserException


class OverrideBlockJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        try:
            return super().get_user(validated_token)
        except AuthenticationFailed as e:
            if e.detail['code'] == 'user_inactive':
                raise BlockUserException()
            else:
                raise e
