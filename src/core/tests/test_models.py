from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_and_name_successfull(self):
        """Test creating a uew user with email and fullname successfully"""
        name = 'Test User'
        email = 'test@email.com'
        password = 'Testpass1234'
        user = get_user_model().objects.create_user(
            name=name, email=email, password=password
        )
        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test the new user email is normalize"""
        email = 'test@EMAIL.COM'
        user = get_user_model().objects.create_user(
            name="Test User", email=email, password="test1234")

        self.assertEqual(user.email, email.lower())

    def test_new_user_with_invalid_email(self):
        """Test new user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                name="Test Name", email=None, password="Test1234")

    def test_create_super_user(self):
        """Test create new super user"""
        user = get_user_model().objects.create_superuser(
            "Test User", "test_supe@email.com", "TestSuper123")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
