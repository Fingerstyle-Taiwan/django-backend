"""
URL mappings for user API.
"""

from django.urls import include, path

from user import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path("token/exchange", views.exchange_token, name="token_exchange"),
    path("verify/<str:uidb64>/<str:token>", views.verify_email, name="verify_email"),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
