from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateCart(TestCase):
    """Test module for creating a cart"""

    def setUp(self) -> None:
        self.user_info = self.generate_user_info()

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

    def test_create_cart(self):
        """Test if a cart is created"""
        user = User.objects.create(**self.user_info)
        cart = user.cart

        self.assertEqual(cart.user, user)
        self.assertEqual(cart.total_price, 0)
        self.assertEqual(cart.created, cart.modified)
