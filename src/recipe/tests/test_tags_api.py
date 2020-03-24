from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test all the publicly available tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retriving tag """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authorized user tag api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'Test User', 'test@domain.com', 'testpassword')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_tag_retrive(self):
        """Retriving tags """
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Tags that only can access authorized users"""
        user2 = get_user_model().objects.create_user(
            'Other User', 'other@domain.com', 'otherpassword')
        Tag.objects.create(user=user2, name='Nonveg')
        tag = Tag.objects.create(user=self.user, name='Fruity')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
