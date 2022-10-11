from django.conf import settings

PROVIDER_NAME = "Facebook"

PROVIDER_SETTINGS = (
    getattr(settings, "SOCIAL_PROVIDERS", {})
    .get("facebook", {})
)

GRAPH_API_VERSION = (
    PROVIDER_SETTINGS
    .get("VERSION", "v15.0")
)
GRAPH_API_URL = "https://graph.facebook.com/" + GRAPH_API_VERSION
GET_PROFILE_API = '/'.join([GRAPH_API_URL, 'me'])
