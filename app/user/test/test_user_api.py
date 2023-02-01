"""
Tests for user API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APIClient

from user.token import generate_token

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    """Crate and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public feature of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test am error is returned if password less than 5 chars."""
        payload = {"email": "test@example.com", "password": "pw", "name": "Test Name"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test generate token for valid credentials."""
        user_detail = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        create_user(**user_detail)

        payload = {
            "email": user_detail["email"],
            "password": user_detail["password"],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credential(self):
        """Test returns error if credentials invalid."""

        create_user(email="test@example.com", password="goodpass")
        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {"email": "test@exmaple.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_user_verifyed(self):
        """Test verify user is verify."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        create_user(**payload)

        user = get_user_model().objects.get(email=payload["email"])
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token.make_token(user)
        VERIFY_URL = reverse(
            "user:verify_email", kwargs={"uidb64": uidb64, "token": token}
        )
        res = self.client.get(VERIFY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.is_verifyed)

    def test_verify_user_not_existed(self):
        """Test verify user isn't existed."""
        uidb64 = "999"
        token = "testtoken"
        VERIFY_URL = reverse(
            "user:verify_email", kwargs={"uidb64": uidb64, "token": token}
        )
        res = self.client.get(VERIFY_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_user_already_verifyed(self):
        """Test verify user already verify."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        create_user(**payload)

        user = get_user_model().objects.get(email=payload["email"])
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token.make_token(user)
        VERIFY_URL = reverse(
            "user:verify_email", kwargs={"uidb64": uidb64, "token": token}
        )

        res = self.client.get(VERIFY_URL)  # first verify
        res = self.client.get(VERIFY_URL)  # second verify

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email="test@example.com", password="testpass123", name="ABC"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {"name": "Updated name", "password": "newpassword123"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
