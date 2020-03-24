from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test user's api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test create user with valid playload"""
        playload = {
            "name": "Test User",
            "email": "test@email.com",
            "password": "test12345"
        }
        res = self.client.post(CREATE_USER_URL, playload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(playload['password']))
        self.assertNotIn('password', res.data)

    def test_existing_user(self):
        """Test created user which is already exist"""
        playload = {
            "name": "Test User",
            "email": "test@email.com",
            "password": "test12345"
        }
        create_user(**playload)
        res = self.client.post(CREATE_USER_URL, playload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 6 chars"""
        playload = {
            "name": "Test User",
            "email": "test@email.com",
            "password": "test"
        }
        res = self.client.post(CREATE_USER_URL, playload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=playload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            "name": "John Doe",
            "email": "john@email.com",
            "password": "john1234"
        }
        create_user(**payload)
        payload_login = {
            "email": "john@email.com",
            "password": "john1234"
        }
        res = self.client.post(CREATE_TOKEN_URL, payload_login)
        self.assertIn('jwt', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Test that token is not created if invalid credential are given"""
        payload = {
            "name": "John Doe",
            "email": "john@email.com",
            "password": "john1234"
        }
        create_user(**payload)
        payload_login = {
            "email": "john4@email.com",
            "password": "john1234"
        }

        res = self.client.post(CREATE_TOKEN_URL, payload_login)
        self.assertNotIn('jwt', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            "email": "jane@email.com",
            "password": "jane12345"
        }

        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertNotIn('jwt', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missing_fields(self):
        """Test that email and password are required"""
        res = self.client.post(
            CREATE_TOKEN_URL, {'email': 'test', 'password': ''})
        self.assertNotIn('jwt', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """Test authentication is required for get user data"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test that require user authentication"""

    def setUp(self):
        user_info = {
            "name": "John Doe",
            "email": "john@email.com",
            "password": "john1234"
        }
        self.user = create_user(**user_info)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_successfull(self):
        """Get user profile data successfully"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email})

    def test_post_me_not_allowed(self):
        """Test post request is not allowed in me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test for updating user profiles info"""
        payload = {
            "name": "Jackob Doe",
            "email": "jack@email.com",
            "password": "jack1234"
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
