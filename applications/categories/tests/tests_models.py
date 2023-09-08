from django.test import TestCase

from ..models import Category


class CreateSingleCategoryTest(TestCase):
    """Test module for Category model."""

    def setUp(self):
        """Set up a method which is used before any test run"""
        self.category_info = self.generate_category_info()

    def generate_category_info(self) -> object:
        return {
            "name": "Test Category",
        }

    def test_create_category(self):
        """Test if category can be created"""
        category = Category.objects.create(**self.category_info)
        self.assertEqual(category.name, self.category_info["name"])
