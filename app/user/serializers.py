'''
Serializers for user API View.
'''


from django.contrib.auth import (get_user_model, authenticate)
from django.utils.translation import gettext as _
from rest_framework import serializers
from core.models import Profile
from user.providers.google.constants import (
    PROVIDER_NAME as GOOGLE_PROVIDER_NAME
)
from user.providers.facebook.constants import (
    PROVIDER_NAME as FACEBOOK_PROVIDER_NAME
)
from datetime import datetime
import string
import secrets


def get_secret_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


class ProfileSerializer(serializers.ModelSerializer):
    ''' Serializer for profile object. '''
    class Meta:
        model = Profile
        fields = ['avatar', 'gender', 'birthdate', 'country',
                  'bio', 'guitar_brand', 'guitar_model']
        read_only_fields = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    ''' Serializer for user object. '''
    profile = ProfileSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'profile']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {
                'write_only': True, 'min_length': 5
                }
            }

    def create(self, validated_data):
        ''' Create and return a user with encrypted password. '''
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        ''' Update and return user. '''
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    ''' Serializer for the user auth token. '''
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        ''' Validate and authenticate the user. '''
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs


class ExchangeProviderSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    provider_name = serializers.CharField(required=True)
    access_token = serializers.CharField(required=True)

    def validate(self, data):
        super(ExchangeProviderSerializer, self).validate(data)
        self.utils = self.load_provider_utils()
        return data

    def login_user_with_token(self):
        user = None
        user_profile = None
        User = get_user_model()

        try:
            email = self.validated_data.get('email')
            user_profile = self.utils.get_user_profile(self.validated_data.get('access_token'))
            if email != user_profile['email']:
                raise Exception("User Email doesn't match")

            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user, is_created = User.objects.update_or_create(
                email=email,
                defaults=self.utils.init_profile_to_user(user_profile)
            )
            user.set_password(get_secret_random_string(10))
            user.save()
        except Exception:
            user = None
            return user

        if user and not user.is_active:
            return None

        user.last_login = datetime.now()
        user.save()

        return user


class ExchangeGoogleSerializer(ExchangeProviderSerializer):
    def load_provider_utils(self):
        from user.providers.google import utils
        return utils

    def validate_provider_name(self, value):
        if GOOGLE_PROVIDER_NAME == value:
            return value

        raise serializers.ValidationError("Provider Name is invalid")


class ExchangeFacebookSerializer(ExchangeProviderSerializer):
    def load_provider_utils(self):
        from user.providers.facebook import utils
        return utils

    def validate_provider_name(self, value):
        if FACEBOOK_PROVIDER_NAME == value:
            return value

        raise serializers.ValidationError("Provider Name is invalid")


PROVIDER_SERIALIZERS = {
    GOOGLE_PROVIDER_NAME: ExchangeGoogleSerializer,
    FACEBOOK_PROVIDER_NAME: ExchangeFacebookSerializer
}