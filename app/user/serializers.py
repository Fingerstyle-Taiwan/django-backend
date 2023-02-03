"""
Serializers for user API View.
"""


import secrets
import string
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import serializers

from core.models import Profile
from user.providers.facebook.constants import PROVIDER_NAME as FACEBOOK_PROVIDER_NAME
from user.providers.google.constants import PROVIDER_NAME as GOOGLE_PROVIDER_NAME
from user.token import generate_token


def get_secret_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


def send_smtp_verify_mail(user):
    mail_subject = "Active your email."

    current_site = settings.EMAIL_CONTENT_DOMAIN
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = generate_token.make_token(user)
    verify_mail_path = reverse(
        "user:verify_email", kwargs={"uidb64": uidb64, "token": token}
    )
    verify_mail_url = f"{current_site}{verify_mail_path}"

    mail_message = render_to_string(
        "verify_email.html",
        {"user": user, "domain": current_site, "verify_mail_url": verify_mail_url},
    )

    mail_recipient = user.email
    email = EmailMessage(
        # title:
        mail_subject,
        # message:
        mail_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        to=[mail_recipient],
    )

    email.fail_silently = False
    email.send()


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    current_site = settings.EMAIL_CONTENT_DOMAIN
    reset_password_path = reverse("user:password_reset:reset-password-confirm")
    reset_password_url = (
        f"{current_site}{reset_password_path}?token={reset_password_token.key}"
    )

    mail_subject = "Reset your password."
    mail_message = render_to_string(
        "user_reset_password.html",
        {
            "current_user": reset_password_token.user,
            "username": reset_password_token.user.name,
            "email": reset_password_token.user.email,
            "reset_password_url": reset_password_url,
        },
    )

    msg = EmailMessage(
        # title:
        mail_subject,
        # message:
        mail_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],
    )
    msg.send()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for profile object."""

    class Meta:
        model = Profile
        fields = [
            "avatar",
            "gender",
            "birthdate",
            "country",
            "bio",
            "guitar_brand",
            "guitar_model",
        ]
        read_only_fields = ["id", "user"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object."""

    profile = ProfileSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name", "profile"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        user = get_user_model().objects.create_user(**validated_data)
        send_smtp_verify_mail(user)

        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

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
            email = self.validated_data.get("email")
            user_profile = self.utils.get_user_profile(
                self.validated_data.get("access_token")
            )
            if email != user_profile["email"]:
                raise Exception("User Email doesn't match")

            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user, is_created = User.objects.update_or_create(
                email=email, defaults=self.utils.init_profile_to_user(user_profile)
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
    FACEBOOK_PROVIDER_NAME: ExchangeFacebookSerializer,
}
