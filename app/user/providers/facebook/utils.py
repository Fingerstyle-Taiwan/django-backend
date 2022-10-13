from user.providers.facebook.constants import (
    PROVIDER_SETTINGS,
    GET_PROFILE_API,
)
import requests
import hmac
import hashlib


def get_app_secret_key():
    return PROVIDER_SETTINGS.get('APP', {}).get('secret', '')


def compute_appsecret_proof(access_token):
    # Generate an appsecret_proof parameter to secure the Graph API call
    # see https://developers.facebook.com/docs/graph-api/securing-requests%20/
    msg = access_token.encode("utf-8")
    key = get_app_secret_key().encode("utf-8")
    appsecret_proof = hmac.new(key, msg, digestmod=hashlib.sha256).hexdigest()
    return appsecret_proof


def get_user_profile(access_token):
    response = requests.get(
        GET_PROFILE_API,
        params={
            "fields": ",".join([
                "id",
                "email",
                "first_name",
                "last_name",
                "middle_name",
                "name",
                "name_format",
                "short_name",
            ]),
            "access_token": access_token,
            "appsecret_proof": compute_appsecret_proof(access_token),
        },
    )
    response.raise_for_status()
    return response.json()


def init_profile_to_user(user_profile):
    return {
        'is_superuser': False,
        'is_staff': False,
        'is_active': True
    }
