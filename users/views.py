from django.http import HttpResponse
from django.views.generic import DetailView

from users.models import UserModel


class UserView(DetailView):
    model = UserModel
    queryset = UserModel.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'


def activate(request, activation_code):
    try:
        UserModel.objects.activate_by_code(activation_code)
        # Todo: redirect to login
        return HttpResponse('Your account has been activated.')
    except Exception as ex:
        return HttpResponse('Wrong activation link')
