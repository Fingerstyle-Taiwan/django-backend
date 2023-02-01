"""
Views for user API.
"""


from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import authentication, generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.settings import api_settings

from core.models import User
from user.serializers import PROVIDER_SERIALIZERS, AuthTokenSerializer, UserSerializer
from user.token import generate_token


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


@api_view(["POST"])
def exchange_token(request):
    try:
        provider_name = request.data.get("provider_name")
        serializer_class = PROVIDER_SERIALIZERS.get(provider_name)
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.login_user_with_token()
        if not user:
            raise Exception("User login failure")

        token, created = Token.objects.update_or_create(user=user)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(data={"access": token.key})


@api_view(["GET"])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception:
        user = None

    if user is None:
        return Response("User not found", status=status.HTTP_400_BAD_REQUEST)

    if user.is_verifyed:
        return Response(
            "Email has already been verified.", status=status.HTTP_400_BAD_REQUEST
        )

    if user and generate_token.check_token(user, token):
        user.is_verifyed = True
        user.save()

        # return redirect('home')
        return Response("Thank you for your email confirmation.")

    return Response("Activation link is invalid!")
