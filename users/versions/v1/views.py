from rest_framework.response import Response
from rest_framework.views import APIView

from users.versions.v1.serializers import UserSerializer


class RetrieveOwnUserView(APIView):
    http_method_names = ['get']

    def get(self, request, **kwargs):
        user = request.user
        return Response(data=UserSerializer(user).data)
