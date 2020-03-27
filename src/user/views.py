from rest_framework import generics, permissions
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenViewBase
from user import serializers


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = serializers.UserSerializer


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = serializers.TokenObtainPairSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrive authenticated user"""
        return self.request.user
