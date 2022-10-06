'''
Serializers for user API View.
'''


from django.contrib.auth import (get_user_model, authenticate)
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _
from rest_framework import serializers
from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    ''' Serializer for profile object. '''
    class Meta:
        model = Profile
        fields = ['avatar', 'gender', 'birthdate', 'country', 'bio', 'guitar_brand', 'guitar_model']
        read_only_fields = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    ''' Serializer for user object. '''
    profile = ProfileSerializer(required=True)
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


class ProfileSerializer(serializers.ModelSerializer):
    ''' Serializer for profile object. '''

    class Meta:
        model = Profile
        read_only_fields = ['user']
