from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import UserModel
from users.versions.v1.classes.controllers.user_auth_controller import UserAuthController


class RegistrationTestCase(APITestCase):
    decoded_token = {'name': 'No Reply Fabula', 'picture': 'https://lh3.googleusercontent.com/a/AATXAJyUyrahDoz28DmvbgBsrk3JOQJI-0R0ZWtDSVjK=s96-c', 'iss': 'https://securetoken.google.com/app-fabula', 'aud': 'app-fabula', 'auth_time': 1629397212, 'user_id': 'egBLlxZRFiTVxUcxvi2jcmPI7zW2', 'sub': 'egBLlxZRFiTVxUcxvi2jcmPI7zW2', 'iat': 1629397212, 'exp': 1629400812, 'email': 'noreply.fabula@gmail.com', 'email_verified': True, 'firebase': {'identities': {'google.com': ['117969712688659268986'], 'email': ['noreply.fabula@gmail.com']}, 'sign_in_provider': 'google.com'}, 'uid': 'egBLlxZRFiTVxUcxvi2jcmPI7zW2'}

    def test_google_first_email_next(self):
        email = self.decoded_token.get('email')
        # Google
        UserAuthController.auth_firebase(self.decoded_token)
        user = UserModel.objects.filter(username=email, email=email).first()
        self.assertIsNotNone(user)

        # Email
        code = user.update_user_confirmation_code()
        response = self.client.post(reverse('v1-auth-by-email'), data={'email': email, 'confirmationCode': code},
                                    format='json')
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_email_first_google_next(self):
        email = self.decoded_token.get('email')
        # Email
        user, _ = UserModel.objects.get_or_create(username=email, email=email)
        code = user.update_user_confirmation_code()
        response = self.client.post(reverse('v1-auth-by-email'), data={'email': email, 'confirmationCode': code},
                                    format='json')
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

        # Google
        email = self.decoded_token.get('email')
        UserAuthController.auth_firebase(self.decoded_token)
        user = UserModel.objects.filter(username=email, email=email).first()
        self.assertIsNotNone(user)
