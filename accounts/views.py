from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from accounts.serializers import RegisterSerializer
from tasks.models import Tasks


class RegisterAPIView(CreateAPIView):
    """
    API to register a new user
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        method to register the user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            'token': token.key,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'incomplete_task': 0,
            'important_task': 0,
        }, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    """
    API used to logout the user
    """
    def post(self, request, format=None):
        """
        method to delete user authentication token to logout the user
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)