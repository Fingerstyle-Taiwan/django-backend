from user.providers.google.constants import (
    GET_PROFILE_API,
)
import requests


def get_user_profile(access_token):
    request = requests.get(
        GET_PROFILE_API,
        params={"access_token": access_token, "alt": "json"},
    )
    request.raise_for_status()
    return request.json()


def init_profile_to_user(user_profile):
    return {
        'is_superuser': False,
        'is_staff': False,
        'is_active': True
    }
