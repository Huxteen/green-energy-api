from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from products.serializers import ProductSerializer
from transactions.serializers import RetrieveTransactionSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ('email',
                  'id',
                  'password',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'state',
                  'address',
                  )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        validated_data.pop('email', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class ListUserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    product = ProductSerializer(many=True, required=False)
    transaction = RetrieveTransactionSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('email',
                  'id',
                  'password',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'state',
                  'address',
                  'product',
                  'transaction',
                  )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication objects"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=True
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Email or Password do not match our record.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for the admin user object."""

    class Meta:
        model = get_user_model()
        fields = ('email',
                  'password',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'state',
                  'address',
                  )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        return get_user_model().objects.create_superuser(**validated_data)
