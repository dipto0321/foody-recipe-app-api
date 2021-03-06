from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def create_sample_user(name="Test",
                       email="test@email.com",
                       password="testpassword"):
    '''Create a sample user'''
    return get_user_model().objects.create_user(name, email, password)


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

    def test_tag_str(self):
        """Test the tag string represent"""
        tag = models.Tag.objects.create(
            user=create_sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=create_sample_user(),
            name='Potato'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=create_sample_user(),
            title='Egg curry',
            making_time_minutes=5,
            price=5.22
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_image_filename_uuid(self, mock_uuid):
        """Test that image is save with proper location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path('None', 'demoimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)
