from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from api_data_science_app.v1.user.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


def create_token_for_exists_users():
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)
        print(user, Token)
