from core.models import Ingredient
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import IngredientSerializer
from rest_framework import status
from rest_framework.test import APIClient


INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    """Test for ingredient publicly available apis"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for access the endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Ingredients can be retrive by authorized user"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'Test User', 'test@domain.com', 'testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_ingredient_retrive(self):
        """Retriving ingredients"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')
        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Ingredient that can only be authorized by authenticated user"""
        user2 = get_user_model().objects.create_user(
            'Other User', 'other@domain.com', 'otherpassword')
        Ingredient.objects.create(user=user2, name='Curliflower')
        ingredient = Ingredient.objects.create(user=self.user, name='Eggplant')
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
