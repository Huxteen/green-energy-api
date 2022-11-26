from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.serializers import (UserSerializer,
                                  AuthTokenSerializer,
                                  AdminUserSerializer)
from utils.renderers import CustomRenderer
from accounts.models import User
from products.models import Product


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer]

    def perform_create(self, serializer):
        """Create User and Product"""
        user = serializer.save()
        product = Product()
        product.user_id = User(pk=user.id)
        product.save()
        return user


class CreateAdminUserView(generics.CreateAPIView):
    " ""Create a new user in the system."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminUserSerializer
    renderer_classes = [CustomRenderer]

    def perform_create(self, serializer):
        """Create User and product"""
        user = serializer.save()
        product = Product()
        product.user_id = User(pk=user.id)
        product.save()
        return user


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = [CustomRenderer]


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomRenderer]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class AdminManageUserDetail(generics.RetrieveUpdateDestroyAPIView):
    """Manage data in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer]


class ListUserAPIView(generics.ListAPIView):
    """Manage data in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = User.objects.filter(is_superuser=False).order_by('-id')
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer]
