from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from ..models import Product
from ..utils import product_photo_file_path
from applications.categories.models import Category

User = get_user_model()


class CreateSingleProductTest(TestCase):
    """Test module for Product model"""

    def setUp(self):
        """Set up a method which is used before any test run"""

        self.product_info = self.generate_product_info()
        self.category_info = self.generate_category_info()
        self.user_info = self.generate_user_info()
        self.photo = self.generate_photo()

    def generate_photo(self):
        return SimpleUploadedFile(
            "test_photo.png", b"file_content", content_type="image/png"
        )

    def generate_product_info(self) -> dict:
        return {
            "name": "Test Product",
            "description": "Test Description",
            "price": 10.23,
            "stock": 10,
            "category": None,
            "owner": None,
            "compare_price": 20.58,
            "is_available": True,
            "photo": self.generate_photo(),
        }

    def generate_category_info(self) -> dict:
        return {
            "name": "Test Category",
        }

    def generate_user_info(self) -> dict:
        return {
            "email": "admin@admin.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "photo": self.generate_photo(),
        }

    def test_create_product(self) -> None:
        # Owner (User) creation
        owner = User.objects.create(**self.user_info)

        # Category creation
        category = Category.objects.create(**self.category_info)

        self.product_info["owner"] = owner
        self.product_info["category"] = category

        product = Product.objects.create(**self.product_info)

        self.assertEqual(product.name, self.product_info["name"])
        self.assertEqual(product.description, self.product_info["description"])
        self.assertEqual(product.price, self.product_info["price"])
        self.assertEqual(product.stock, self.product_info["stock"])
