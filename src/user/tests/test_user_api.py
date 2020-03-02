from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')


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
        self.assertIn('token', res.data)
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
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            "email": "jane@email.com",
            "password": "jane12345"
        }

        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and password are required"""
        res = self.client.post(
            CREATE_TOKEN_URL, {'email': 'test', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
