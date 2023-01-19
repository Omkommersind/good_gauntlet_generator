from django.views.generic import DetailView

from users.models import UserModel


class UserView(DetailView):
    model = UserModel
    queryset = UserModel.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'
