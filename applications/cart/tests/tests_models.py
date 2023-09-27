from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from applications.cart.models import CartItem
from applications.categories.models import Category
from applications.products.models import Product

User = get_user_model()


class CreateCart(TestCase):
    """Test module for creating a cart"""

    def setUp(self) -> None:
        self.user_info = self.generate_user_info()
        self.product_info = self.generate_product_info()
        self.category_info = self.generate_category_info()
        self.photo = self.generate_photo()

    def generate_user_info(self) -> dict:
        return {
            "email": "admin@admin.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
        }

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

    def test_create_cart(self):
        """Test if a cart is created"""
        user = User.objects.create(**self.user_info)
        cart = user.cart

        self.assertEqual(cart.user, user)
        self.assertEqual(cart.total_price, 0)
        self.assertEqual(cart.total_items, 0)
        self.assertEqual(cart.created, cart.modified)

    def test_create_cart_item(self):
        """Test cart items creation"""
        user = User.objects.create(**self.user_info)
        cart = user.cart

        # Category creation
        category = Category.objects.create(**self.category_info)

        self.product_info["owner"] = user
        self.product_info["category"] = category

        product = Product.objects.create(**self.product_info)

        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.partial_price, product.price * 2)
        self.assertEqual(cart_item.created, cart_item.modified)
